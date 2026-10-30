"""
Ameetech Bulk Flyer Generation Tool
Core Generation Engine and Batch Orchestrator.
"""
import os
import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from flyer_tool.config import (
    ROOT_DIR,
    PROMPTS_DIR,
    GENERATED_DIR,
    APPROVED_DIR,
    FAILED_DIR,
    DEFAULT_PROMPTS_JSON,
    DEFAULT_PROMPTS_CSV,
    DEFAULT_REPORT_JSON,
    DEFAULT_REPORT_MD,
    get_concurrency,
    get_max_retries,
    get_batch_size,
    DEFAULT_IMAGE_WIDTH,
    DEFAULT_IMAGE_HEIGHT
)
from flyer_tool.models import FlyerPrompt, GenerationRecord, load_prompts_file, save_prompts_file
from flyer_tool.providers import get_provider, BaseProvider
from flyer_tool.gallery import generate_preview_gallery

class FlyerEngine:
    def __init__(self):
        self.ensure_directories()

    @staticmethod
    def ensure_directories():
        """Create generated/, approved/, failed/, and prompts/ directories automatically."""
        for d in (PROMPTS_DIR, GENERATED_DIR, APPROVED_DIR, FAILED_DIR):
            d.mkdir(parents=True, exist_ok=True)

    def validate_prompts(self, prompts: List[FlyerPrompt]) -> Tuple[bool, List[str]]:
        """
        Validate all prompt records for schema, duplicate IDs, and duplicate filenames.
        Ensures original prompts are preserved and not empty.
        """
        errors = []
        seen_ids = set()
        seen_filenames = set()

        for idx, p in enumerate(prompts, start=1):
            p_errors = p.validate()
            if p_errors:
                errors.extend(p_errors)
            
            # Check ID uniqueness
            norm_id = p.id.strip().upper()
            if norm_id in seen_ids:
                errors.append(f"Duplicate Prompt ID found at item {idx}: '{p.id}'.")
            seen_ids.add(norm_id)

            # Check Filename uniqueness
            norm_fname = p.filename.strip().lower()
            if norm_fname in seen_filenames:
                errors.append(f"Duplicate Filename found at item {idx}: '{p.filename}'.")
            seen_filenames.add(norm_fname)

        return len(errors) == 0, errors

    def dry_run(
        self,
        prompts_file: Path = DEFAULT_PROMPTS_JSON,
        provider_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate prompts, paths, and provider credentials without spending any API credits.
        """
        self.ensure_directories()

        if not prompts_file.exists():
            return {
                "success": False,
                "error": f"Prompts file does not exist at {prompts_file}",
                "prompts_count": 0
            }

        try:
            prompts = load_prompts_file(prompts_file)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to parse prompts file: {str(e)}",
                "prompts_count": 0
            }

        valid, validation_errors = self.validate_prompts(prompts)
        
        # Check provider
        provider = get_provider(provider_name)
        cred_ok, cred_msg = provider.validate_credentials()
        cost_info = provider.get_cost_info()

        # Check existing filesystem status
        already_generated = []
        already_approved = []
        pending = []

        for p in prompts:
            gen_path = GENERATED_DIR / p.filename
            app_path = APPROVED_DIR / p.filename
            if app_path.exists():
                already_approved.append(p.id)
            elif gen_path.exists():
                already_generated.append(p.id)
            else:
                pending.append(p.id)

        report = {
            "success": valid and cred_ok,
            "validation_errors": validation_errors,
            "provider": provider.name,
            "provider_credentials_ok": cred_ok,
            "provider_status_message": cred_msg,
            "cost_info": cost_info,
            "total_prompts": len(prompts),
            "pending_count": len(pending),
            "already_generated_count": len(already_generated),
            "already_approved_count": len(already_approved),
            "directories_ready": {
                "prompts": str(PROMPTS_DIR),
                "generated": str(GENERATED_DIR),
                "approved": str(APPROVED_DIR),
                "failed": str(FAILED_DIR)
            }
        }
        return report

    def _generate_single_with_retry(
        self,
        prompt: FlyerPrompt,
        provider: BaseProvider,
        force: bool,
        max_retries: int
    ) -> GenerationRecord:
        """Process a single prompt with retry logic and exact filename preservation."""
        output_file = GENERATED_DIR / prompt.filename
        app_file = APPROVED_DIR / prompt.filename
        
        # Check if already approved
        if app_file.exists() and not force:
            return GenerationRecord(
                id=prompt.id,
                filename=prompt.filename,
                status="approved",
                provider=provider.name,
                timestamp=datetime.utcnow().isoformat() + "Z",
                duration_seconds=0.0,
                error=None,
                output_path=str(app_file),
                retries_used=0
            )

        # Skip if already generated and not forced
        if output_file.exists() and not force:
            return GenerationRecord(
                id=prompt.id,
                filename=prompt.filename,
                status="generated",
                provider=provider.name,
                timestamp=datetime.utcnow().isoformat() + "Z",
                duration_seconds=0.0,
                error=None,
                output_path=str(output_file),
                retries_used=0
            )

        start_time = time.time()
        last_error = None
        retries_used = 0

        for attempt in range(max_retries + 1):
            if attempt > 0:
                retries_used += 1
                backoff = 1.5 ** attempt
                time.sleep(backoff)

            success, err_msg = provider.generate(
                prompt=prompt,
                output_path=output_file,
                width=DEFAULT_IMAGE_WIDTH,
                height=DEFAULT_IMAGE_HEIGHT
            )

            if success:
                duration = round(time.time() - start_time, 2)
                return GenerationRecord(
                    id=prompt.id,
                    filename=prompt.filename,
                    status="generated",
                    provider=provider.name,
                    timestamp=datetime.utcnow().isoformat() + "Z",
                    duration_seconds=duration,
                    error=None,
                    output_path=str(output_file),
                    retries_used=retries_used
                )
            else:
                last_error = err_msg

        duration = round(time.time() - start_time, 2)
        return GenerationRecord(
            id=prompt.id,
            filename=prompt.filename,
            status="failed",
            provider=provider.name,
            timestamp=datetime.utcnow().isoformat() + "Z",
            duration_seconds=duration,
            error=last_error or "Unknown failure",
            output_path=None,
            retries_used=retries_used
        )

    def process_batch(
        self,
        prompts_file: Path = DEFAULT_PROMPTS_JSON,
        provider_name: Optional[str] = None,
        batch_size: Optional[int] = None,
        concurrency: Optional[int] = None,
        force: bool = False,
        dry_run: bool = False,
        specific_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute flyer generation in controlled batches with concurrency, retries,
        and progress reporting.
        """
        self.ensure_directories()

        if dry_run:
            print("\n🔍 EXECUTING DRY-RUN MODE (No API calls or credits spent)...")
            report = self.dry_run(prompts_file, provider_name)
            return report

        # Load prompts
        all_prompts = load_prompts_file(prompts_file)
        valid, errors = self.validate_prompts(all_prompts)
        if not valid:
            raise ValueError(f"Prompt validation failed:\n" + "\n".join(errors))

        # Filter by specific ID if requested, while retaining all_prompts for persistence
        if specific_id:
            prompts = [p for p in all_prompts if p.id.lower() == specific_id.lower() or p.filename.lower() == specific_id.lower()]
            if not prompts:
                raise ValueError(f"No prompt found matching ID or filename '{specific_id}'")
        else:
            prompts = all_prompts

        # Resolve provider
        provider = get_provider(provider_name)
        cred_ok, cred_msg = provider.validate_credentials()
        if not cred_ok:
            raise RuntimeError(
                f"Provider '{provider.name}' cannot be used because credentials are missing or invalid:\n"
                f"{cred_msg}\n\n"
                f"TIP: You can use the local branded generator without API keys: --provider local\n"
                f"Or provide credentials in .env (e.g., OPENAI_API_KEY, STABILITY_API_KEY, GEMINI_API_KEY)."
            )

        n_workers = concurrency or get_concurrency()
        b_size = batch_size or get_batch_size()
        max_retries = get_max_retries()

        print(f"\n🚀 Starting Ameetech Bulk Flyer Generation")
        print(f"   Provider:      {provider.name}")
        print(f"   Prompts count: {len(prompts)}")
        print(f"   Concurrency:   {n_workers}")
        print(f"   Batch size:    {b_size}")
        print(f"   Force rerun:   {force}")
        print(f"   Output dir:    {GENERATED_DIR}\n")

        records: List[GenerationRecord] = []
        total = len(prompts)
        completed = 0
        skipped = 0
        failed = 0

        # Split into batches
        for batch_idx in range(0, total, b_size):
            batch = prompts[batch_idx: batch_idx + b_size]
            current_batch_num = (batch_idx // b_size) + 1
            total_batches = (total + b_size - 1) // b_size
            print(f"--- Processing Batch [{current_batch_num}/{total_batches}] ({len(batch)} items) ---")

            with ThreadPoolExecutor(max_workers=n_workers) as executor:
                future_to_prompt = {
                    executor.submit(
                        self._generate_single_with_retry,
                        p,
                        provider,
                        force,
                        max_retries
                    ): p for p in batch
                }

                for future in as_completed(future_to_prompt):
                    prompt_item = future_to_prompt[future]
                    try:
                        record = future.result()
                    except Exception as exc:
                        record = GenerationRecord(
                            id=prompt_item.id,
                            filename=prompt_item.filename,
                            status="failed",
                            provider=provider.name,
                            timestamp=datetime.utcnow().isoformat() + "Z",
                            error=str(exc)
                        )

                    records.append(record)
                    completed += 1

                    # Update in-memory prompt status
                    prompt_item.status = record.status

                    if record.status in ("generated", "approved"):
                        if record.duration_seconds == 0.0 and not force:
                            skipped += 1
                            status_desc = "SKIPPED (Already exists)"
                        else:
                            status_desc = f"GENERATED ({record.duration_seconds}s)"
                        print(f"[{completed}/{total}] {record.id} ({record.filename}) -> {status_desc}")
                    else:
                        failed += 1
                        print(f"[{completed}/{total}] {record.id} ({record.filename}) -> FAILED: {record.error}")

        # Save updated prompt statuses back to JSON and CSV
        save_prompts_file(all_prompts, prompts_file)
        if prompts_file == DEFAULT_PROMPTS_JSON and DEFAULT_PROMPTS_CSV.exists():
            save_prompts_file(all_prompts, DEFAULT_PROMPTS_CSV)
        elif prompts_file == DEFAULT_PROMPTS_CSV and DEFAULT_PROMPTS_JSON.exists():
            save_prompts_file(all_prompts, DEFAULT_PROMPTS_JSON)

        # Save generation report
        report_data = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "provider": provider.name,
            "total_prompts": total,
            "generated_count": sum(1 for r in records if r.status in ("generated", "approved")),
            "skipped_count": skipped,
            "failed_count": failed,
            "records": [r.to_dict() for r in records]
        }

        with open(DEFAULT_REPORT_JSON, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Save Markdown Report
        self._write_markdown_report(report_data, DEFAULT_REPORT_MD)

        # Refresh preview gallery
        generate_preview_gallery(all_prompts, report_data)

        print(f"\n✨ Generation Finished:")
        print(f"   Success/Approved: {report_data['generated_count']}/{total}")
        print(f"   Skipped:          {skipped}")
        print(f"   Failed:           {failed}")
        print(f"   Report JSON:      {DEFAULT_REPORT_JSON}")
        print(f"   Report Markdown:  {DEFAULT_REPORT_MD}")
        print(f"   Preview Gallery:  file://{ROOT_DIR / 'preview_gallery.html'}\n")

        return report_data

    def _write_markdown_report(self, data: Dict[str, Any], output_path: Path):
        """Generate a clean markdown report."""
        lines = [
            f"# Ameetech Bulk Flyer Generation Report",
            f"",
            f"- **Timestamp**: `{data['generated_at']}`",
            f"- **Provider**: `{data['provider']}`",
            f"- **Total Prompts**: `{data['total_prompts']}`",
            f"- **Successful/Existing**: `{data['generated_count']}`",
            f"- **Skipped**: `{data['skipped_count']}`",
            f"- **Failed**: `{data['failed_count']}`",
            f"",
            f"## Itemized Records",
            f"",
            f"| ID | Filename | Status | Duration | Retries | Error Details |",
            f"|---|---|---|---|---|---|"
        ]
        for r in data["records"]:
            err = r.get("error") or "—"
            err_sanitized = str(err).replace("|", "\\|")
            dur = f"{r.get('duration_seconds', 0.0):.2f}s"
            lines.append(f"| {r['id']} | `{r['filename']}` | **{r['status']}** | {dur} | {r.get('retries_used', 0)} | {err_sanitized} |")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
