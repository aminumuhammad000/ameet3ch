"""
Unit and Integration Tests for Ameetech Bulk Flyer Generation Tool.
Part of the Ameetech engineering test suite.
"""
import unittest
import os
import shutil
import tempfile
import json
from pathlib import Path
from PIL import Image

from flyer_tool.config import (
    ROOT_DIR,
    PROMPTS_DIR,
    GENERATED_DIR,
    APPROVED_DIR,
    FAILED_DIR,
    DEFAULT_PROMPTS_JSON,
    DEFAULT_PROMPTS_CSV,
    COLOR_PRIMARY,
    get_logo_path
)
from flyer_tool.models import (
    FlyerPrompt,
    load_prompts_file,
    save_prompts_file,
    SAFE_FILENAME_REGEX
)
from flyer_tool.providers import (
    get_provider,
    BaseProvider,
    MockProvider,
    LocalBrandedProvider,
    OpenAIProvider,
    StabilityAIProvider,
    GoogleImagenProvider
)
from flyer_tool.engine import FlyerEngine
from flyer_tool.approval import approve_flyer, approve_all, reject_flyer
from flyer_tool.gallery import generate_preview_gallery


class TestFlyerPromptValidation(unittest.TestCase):
    """Tests for prompt validation, schema integrity, and Ameetech branding adherence."""

    def test_json_prompts_file_exists_and_contains_30_prompts(self):
        self.assertTrue(DEFAULT_PROMPTS_JSON.exists(), f"Prompts JSON not found at {DEFAULT_PROMPTS_JSON}")
        prompts = load_prompts_file(DEFAULT_PROMPTS_JSON)
        self.assertEqual(len(prompts), 30, f"Expected exactly 30 prompts, found {len(prompts)}")

    def test_csv_prompts_file_exists_and_matches_count(self):
        self.assertTrue(DEFAULT_PROMPTS_CSV.exists(), f"Prompts CSV not found at {DEFAULT_PROMPTS_CSV}")
        prompts = load_prompts_file(DEFAULT_PROMPTS_CSV)
        self.assertEqual(len(prompts), 30, f"Expected exactly 30 prompts in CSV, found {len(prompts)}")

    def test_all_prompts_have_unique_ids_and_filenames(self):
        prompts = load_prompts_file(DEFAULT_PROMPTS_JSON)
        ids = [p.id for p in prompts]
        filenames = [p.filename for p in prompts]

        self.assertEqual(len(ids), len(set(ids)), "Duplicate prompt IDs detected")
        self.assertEqual(len(filenames), len(set(filenames)), "Duplicate filenames detected")

    def test_all_filenames_are_safe_and_square_png(self):
        prompts = load_prompts_file(DEFAULT_PROMPTS_JSON)
        for p in prompts:
            self.assertTrue(p.filename.endswith(".png"), f"Filename {p.filename} must end in .png")
            self.assertRegex(p.filename, SAFE_FILENAME_REGEX, f"Filename {p.filename} contains invalid characters")
            self.assertNotIn("/", p.filename)
            self.assertNotIn("\\", p.filename)
            self.assertNotIn("..", p.filename)

    def test_all_prompts_contain_ameetech_brand_requirements(self):
        prompts = load_prompts_file(DEFAULT_PROMPTS_JSON)
        for p in prompts:
            # Check contact fields
            self.assertEqual(p.website, "ameetechnology.com.ng")
            self.assertEqual(p.whatsapp, "+234 810 001 5498")
            
            # Check prompt length and quality
            self.assertGreaterEqual(len(p.image_prompt), 50, f"Prompt {p.id} too short")
            self.assertIn("Ameetech", p.image_prompt, f"Prompt {p.id} must reference Ameetech brand")
            self.assertIn("purple", p.image_prompt.lower(), f"Prompt {p.id} must specify purple brand accents")

    def test_invalid_prompt_validation_errors(self):
        bad_prompt = FlyerPrompt(
            id="",
            title="",
            filename="../../invalid.exe",
            image_prompt="short",
            status="unknown_status"
        )
        errors = bad_prompt.validate()
        self.assertGreaterEqual(len(errors), 4)


class TestDirectoryStructureAndEngine(unittest.TestCase):
    """Tests for automatic directory creation, dry-run, and batching."""

    def setUp(self):
        self.engine = FlyerEngine()

    def test_directories_created_automatically(self):
        self.engine.ensure_directories()
        self.assertTrue(PROMPTS_DIR.exists())
        self.assertTrue(GENERATED_DIR.exists())
        self.assertTrue(APPROVED_DIR.exists())
        self.assertTrue(FAILED_DIR.exists())

    def test_dry_run_does_not_spend_credits_or_create_images(self):
        report = self.engine.dry_run(DEFAULT_PROMPTS_JSON, provider_name="mock")
        self.assertTrue(report["success"])
        self.assertEqual(report["total_prompts"], 30)
        self.assertIn("cost_info", report)
        self.assertIn("directories_ready", report)

    def test_logo_asset_discovery(self):
        logo = get_logo_path()
        self.assertTrue(logo.exists(), f"Ameetech logo not found at {logo}")
        with Image.open(logo) as im:
            self.assertIn(im.format.upper(), ("PNG", "JPEG", "WEBP"))


class TestProviderAdapters(unittest.TestCase):
    """Tests for provider adapter abstractions and local image compositor."""

    def test_provider_factory(self):
        p_mock = get_provider("mock")
        self.assertIsInstance(p_mock, MockProvider)
        
        p_local = get_provider("local")
        self.assertIsInstance(p_local, LocalBrandedProvider)

        with self.assertRaises(ValueError):
            get_provider("non_existent_provider_123")

    def test_local_branded_provider_generates_valid_1080x1080_png(self):
        temp_dir = tempfile.mkdtemp()
        try:
            out_file = Path(temp_dir) / "test_brand_flyer.png"
            prompt = FlyerPrompt(
                id="TEST-001",
                title="Enterprise Cloud Solutions",
                category="Cloud & DevOps",
                filename="test_brand_flyer.png",
                image_prompt="Clean white background with vibrant purple Ameetech accents",
                status="pending"
            )
            provider = LocalBrandedProvider()
            success, err = provider.generate(prompt, out_file, width=1080, height=1080)
            
            self.assertTrue(success, f"Local render failed: {err}")
            self.assertTrue(out_file.exists())
            
            with Image.open(out_file) as im:
                self.assertEqual(im.size, (1080, 1080), "Output flyer must be exactly 1080x1080")
                self.assertEqual(im.format, "PNG")
        finally:
            shutil.rmtree(temp_dir)

    def test_openai_provider_credential_check_when_missing(self):
        old_key = os.environ.get("OPENAI_API_KEY")
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        try:
            provider = OpenAIProvider()
            # If no key, should fail validation gracefully
            ok, msg = provider.validate_credentials()
            if not provider.api_key:
                self.assertFalse(ok)
                self.assertIn("Missing OPENAI_API_KEY", msg)
        finally:
            if old_key:
                os.environ["OPENAI_API_KEY"] = old_key


class TestApprovalWorkflow(unittest.TestCase):
    """Tests that images are NEVER auto-published and require explicit approval."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.prompts_json = Path(self.temp_dir) / "test_prompts.json"
        self.prompts = [
            FlyerPrompt(
                id="FLY-TEST-1",
                title="Fintech Engine",
                category="Fintech",
                filename="fly-test-1.png",
                image_prompt="Ameetech modern fintech flyer"
            ),
            FlyerPrompt(
                id="FLY-TEST-2",
                title="AI Portal",
                category="AI",
                filename="fly-test-2.png",
                image_prompt="Ameetech modern AI flyer"
            )
        ]
        save_prompts_file(self.prompts, self.prompts_json)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_approval_workflow_requires_image_and_copies_to_approved(self):
        # Create dummy image in generated/
        gen_img = GENERATED_DIR / "fly-test-1.png"
        app_img = APPROVED_DIR / "fly-test-1.png"
        if app_img.exists():
            app_img.unlink()

        # Simulate generated image
        Image.new("RGB", (100, 100), color="purple").save(gen_img)

        try:
            # 1. Image is not yet in approved/
            self.assertFalse(app_img.exists())

            # 2. Approve flyer
            ok, msg = approve_flyer("FLY-TEST-1", prompts_file=self.prompts_json)
            self.assertTrue(ok)
            self.assertTrue(app_img.exists(), "Approved image must be copied to approved/ folder")

            # 3. Verify status updated
            updated_prompts = load_prompts_file(self.prompts_json)
            self.assertEqual(updated_prompts[0].status, "approved")
        finally:
            if gen_img.exists(): gen_img.unlink()
            if app_img.exists(): app_img.unlink()

    def test_cannot_approve_ungenerated_image(self):
        ok, msg = approve_flyer("FLY-TEST-2", prompts_file=self.prompts_json)
        self.assertFalse(ok)
        self.assertIn("has not been generated yet", msg)


class TestGalleryGeneration(unittest.TestCase):
    """Tests for HTML preview gallery generation."""

    def test_preview_gallery_html_generation(self):
        temp_dir = tempfile.mkdtemp()
        try:
            out_gallery = Path(temp_dir) / "test_gallery.html"
            prompts = load_prompts_file(DEFAULT_PROMPTS_JSON)
            res = generate_preview_gallery(prompts, output_path=out_gallery)
            
            self.assertTrue(out_gallery.exists())
            with open(out_gallery, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("Ameetech Flyer Review", content)
                self.assertIn("#6C2BD9", content)
                self.assertIn("ameetechnology.com.ng", content)
                self.assertIn("+234 810 001 5498", content)
                self.assertIn("FLYER-001", content)
                self.assertIn("FLYER-030", content)
        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
