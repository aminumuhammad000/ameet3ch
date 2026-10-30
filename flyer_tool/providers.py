"""
Ameetech Bulk Flyer Generation Tool
Configurable Image Generation Provider Adapters.
"""
from abc import ABC, abstractmethod
import os
import sys
import time
import base64
import json
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import urllib.request
import urllib.error

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from flyer_tool.config import (
    ROOT_DIR,
    COLOR_PRIMARY,
    COLOR_PRIMARY_DARK,
    COLOR_ACCENT_TINT,
    COLOR_ACCENT_PINK,
    COLOR_BG_WHITE,
    COLOR_TEXT_MAIN,
    COLOR_TEXT_MUTED,
    COLOR_BORDER,
    DEFAULT_IMAGE_WIDTH,
    DEFAULT_IMAGE_HEIGHT,
    get_logo_path,
    get_env_var
)
from flyer_tool.models import FlyerPrompt

# Font helper to find available system fonts
def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidate_paths = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


class BaseProvider(ABC):
    """Abstract base class for all flyer generation providers."""
    name: str = "base"

    @abstractmethod
    def validate_credentials(self) -> Tuple[bool, str]:
        """Check whether required API keys and settings exist."""
        pass

    @abstractmethod
    def generate(
        self,
        prompt: FlyerPrompt,
        output_path: Path,
        width: int = DEFAULT_IMAGE_WIDTH,
        height: int = DEFAULT_IMAGE_HEIGHT
    ) -> Tuple[bool, Optional[str]]:
        """
        Generate image file and save to output_path.
        Returns: (success: bool, error_message: Optional[str])
        """
        pass

    def get_cost_info(self) -> Dict[str, Any]:
        """Estimated cost and quota limitations."""
        return {
            "provider": self.name,
            "cost_per_image_usd": 0.0,
            "estimated_30_batch_cost_usd": 0.0,
            "notes": "Cost estimate not configured."
        }


class LocalBrandedProvider(BaseProvider):
    """
    High-fidelity local branded flyer compositor.
    Generates genuine 1080x1080 PNG flyers strictly adhering to Ameetech brand guidelines:
    - White background with bold purple accents (#6C2BD9)
    - Authentic Ameetech logo asset integration
    - Clear typography hierarchy optimized for mobile
    - Official website (ameetechnology.com.ng) and WhatsApp (+234 810 001 5498)
    - Zero API cost, reliable, fully offline capable.
    """
    name = "local"

    def validate_credentials(self) -> Tuple[bool, str]:
        logo_path = get_logo_path()
        if not logo_path.exists():
            return True, f"Local provider ready (Note: Logo file {logo_path.name} not found, text fallback will be used)."
        return True, f"Local provider ready. Logo located at: {logo_path}"

    def get_cost_info(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "cost_per_image_usd": 0.00,
            "estimated_30_batch_cost_usd": 0.00,
            "quota_limit": "Unlimited (Local Machine)",
            "notes": "Generates branded 1080x1080 flyers directly on device using Pillow and local assets without spending API credits."
        }

    def _hex_to_rgb(self, hex_code: str) -> Tuple[int, int, int]:
        h = hex_code.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _draw_gradient_mesh(self, img: Image.Image, width: int, height: int):
        """Draw subtle Ameetech brand curves and purple geometric accents."""
        draw = ImageDraw.Draw(img, "RGBA")
        c_primary = self._hex_to_rgb(COLOR_PRIMARY)
        c_tint = self._hex_to_rgb(COLOR_ACCENT_TINT)

        # Top-right decorative modern geometric polygon
        draw.polygon([(width - 320, 0), (width, 0), (width, 320)], fill=(c_tint[0], c_tint[1], c_tint[2], 80))
        draw.polygon([(width - 240, 0), (width, 0), (width, 240)], fill=(c_primary[0], c_primary[1], c_primary[2], 25))
        draw.polygon([(width - 140, 0), (width, 0), (width, 140)], fill=(c_primary[0], c_primary[1], c_primary[2], 40))

        # Subtle bottom-left accent arc
        draw.pieslice([-100, height - 350, 250, height], 270, 360, fill=(c_tint[0], c_tint[1], c_tint[2], 60))
        
        # Subtle horizontal guideline
        draw.line([(60, 210), (width - 60, 210)], fill=(226, 232, 240, 255), width=2)

    def generate(
        self,
        prompt: FlyerPrompt,
        output_path: Path,
        width: int = DEFAULT_IMAGE_WIDTH,
        height: int = DEFAULT_IMAGE_HEIGHT
    ) -> Tuple[bool, Optional[str]]:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 1. Base Canvas (1080x1080 White)
            img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
            
            # 2. Subtle Gradient Accents & Geometric Brand Touches
            self._draw_gradient_mesh(img, width, height)
            
            draw = ImageDraw.Draw(img)

            # Colors
            c_primary = self._hex_to_rgb(COLOR_PRIMARY)
            c_primary_dark = self._hex_to_rgb(COLOR_PRIMARY_DARK)
            c_tint = self._hex_to_rgb(COLOR_ACCENT_TINT)
            c_text_main = self._hex_to_rgb(COLOR_TEXT_MAIN)
            c_text_muted = self._hex_to_rgb(COLOR_TEXT_MUTED)

            # 3. Header: Ameetech Logo & Brand Tagline
            logo_path = get_logo_path()
            logo_placed = False
            if logo_path.exists():
                try:
                    logo_im = Image.open(logo_path).convert("RGBA")
                    # Fit logo to 140x140 max
                    logo_im.thumbnail((140, 140), Image.Resampling.LANCZOS)
                    lw, lh = logo_im.size
                    img.paste(logo_im, (70, 50), mask=logo_im)
                    logo_placed = True
                except Exception:
                    logo_placed = False

            # Brand Wordmark
            brand_font = get_font(38, bold=True)
            brand_sub_font = get_font(20, bold=False)
            text_x = 230 if logo_placed else 70
            draw.text((text_x, 62), "AMEETECH", fill=c_primary, font=brand_font)
            draw.text((text_x, 112), "ENTERPRISE SOFTWARE & DIGITAL AUTOMATION", fill=c_text_muted, font=brand_sub_font)

            # Top Right: Flyer ID / Quality Badge
            id_font = get_font(18, bold=True)
            badge_text = f"ID: {prompt.id}"
            badge_w = len(badge_text) * 12 + 24
            badge_rect = [width - 70 - badge_w, 75, width - 70, 115]
            draw.rounded_rectangle(badge_rect, radius=8, fill=c_tint, outline=c_primary, width=1)
            draw.text((width - 70 - badge_w + 12, 85), badge_text, fill=c_primary, font=id_font)

            # 4. Category Tag
            cat_font = get_font(22, bold=True)
            cat_text = f"●  {prompt.category.upper()}"
            cat_box = [70, 240, 70 + len(cat_text) * 15 + 30, 280]
            draw.rounded_rectangle(cat_box, radius=6, fill=c_tint)
            draw.text((85, 248), cat_text, fill=c_primary, font=cat_font)

            # 5. Main Title (Bold, readable hierarchy, word-wrapped)
            title_font = get_font(44, bold=True)
            words = prompt.title.split()
            lines = []
            curr_line = ""
            for w in words:
                test_line = f"{curr_line} {w}".strip()
                if len(test_line) > 30 and curr_line:
                    lines.append(curr_line)
                    curr_line = w
                else:
                    curr_line = test_line
            if curr_line:
                lines.append(curr_line)

            y_text = 305
            for line in lines[:3]:  # Max 3 lines
                draw.text((70, y_text), line, fill=c_text_main, font=title_font)
                y_text += 55

            # 6. Central Visual Graphic Box (Modern Card with Illustration Motif)
            card_top = max(y_text + 20, 480)
            card_bottom = height - 170
            card_rect = [70, card_top, width - 70, card_bottom]
            
            # Subtle card shadow
            shadow_rect = [card_rect[0] + 4, card_rect[1] + 4, card_rect[2] + 4, card_rect[3] + 4]
            draw.rounded_rectangle(shadow_rect, radius=20, fill=(235, 238, 244, 180))
            # Card body
            draw.rounded_rectangle(card_rect, radius=20, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
            
            # Decorative purple gradient strip on top of card
            draw.rounded_rectangle([card_rect[0], card_rect[1], card_rect[2], card_rect[1] + 12], radius=6, fill=c_primary)

            # Center Illustration Motif inside card
            center_cx = (card_rect[0] + card_rect[2]) // 2
            center_cy = (card_rect[1] + card_rect[3]) // 2 - 25

            # Outer concentric rings
            for r in (110, 80, 50):
                draw.ellipse([center_cx - r, center_cy - r, center_cx + r, center_cy + r], outline=c_tint, width=3)
            
            # Tech node circle
            draw.ellipse([center_cx - 38, center_cy - 38, center_cx + 38, center_cy + 38], fill=c_primary)
            draw.ellipse([center_cx - 16, center_cy - 16, center_cx + 16, center_cy + 16], fill=(255, 255, 255, 255))

            # Connected tech satellite dots
            satellites = [(center_cx - 80, center_cy - 50), (center_cx + 80, center_cy - 50),
                          (center_cx - 95, center_cy + 40), (center_cx + 95, center_cy + 40)]
            for sx, sy in satellites:
                draw.line([(center_cx, center_cy), (sx, sy)], fill=c_tint, width=2)
                draw.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=c_primary_dark)

            # Key capability caption below the motif
            core_font = get_font(24, bold=True)
            core_sub_font = get_font(18, bold=False)
            draw.text((center_cx - 180, center_cy + 105), "High-Performance Nigerian Engineering", fill=c_text_main, font=core_font)
            draw.text((center_cx - 160, center_cy + 140), "Modern Architecture • Scalable • Cloud-Ready", fill=c_text_muted, font=core_sub_font)

            # 7. Bottom Brand Footer Banner
            footer_h = 110
            footer_top = height - footer_h
            
            # Solid Ameetech purple footer banner
            draw.rectangle([0, footer_top, width, height], fill=c_primary)

            # Left side: Website
            web_font = get_font(24, bold=True)
            draw.text((70, footer_top + 40), f"🌐  {prompt.website}", fill=(255, 255, 255, 255), font=web_font)

            # Right side: WhatsApp
            wa_font = get_font(24, bold=True)
            wa_text = f"💬  WhatsApp: {prompt.whatsapp}"
            draw.text((width - 440, footer_top + 40), wa_text, fill=(255, 255, 255, 255), font=wa_font)

            # Top thin accent line of footer
            draw.line([(0, footer_top), (width, footer_top)], fill=(255, 130, 169, 255), width=4)

            # Save PNG
            final_img = img.convert("RGB")
            final_img.save(output_path, "PNG", optimize=True)
            return True, None

        except Exception as e:
            return False, f"Local render failed: {str(e)}"


class OpenAIProvider(BaseProvider):
    """
    OpenAI DALL-E Image Generation Provider.
    Supports DALL-E 3 (1024x1024, rescaled to 1080x1080).
    Requires OPENAI_API_KEY environment variable.
    """
    name = "openai"

    def __init__(self):
        self.api_key = get_env_var("OPENAI_API_KEY")
        self.model = get_env_var("OPENAI_IMAGE_MODEL", "dall-e-3")

    def validate_credentials(self) -> Tuple[bool, str]:
        if not self.api_key:
            return False, "Missing OPENAI_API_KEY in environment or .env."
        if not self.api_key.startswith("sk-"):
            return False, "OPENAI_API_KEY appears malformed (expected to start with 'sk-')."
        return True, f"OpenAI credentials configured (model: {self.model})."

    def get_cost_info(self) -> Dict[str, Any]:
        cost_per_img = 0.040 if self.model == "dall-e-3" else 0.020
        return {
            "provider": self.name,
            "model": self.model,
            "cost_per_image_usd": cost_per_img,
            "estimated_30_batch_cost_usd": round(cost_per_img * 30, 2),
            "quota_limit": "Standard tier limits apply (check platform.openai.com/account/limits)",
            "notes": "Requires prepaid billing credit in your OpenAI developer account."
        }

    def generate(
        self,
        prompt: FlyerPrompt,
        output_path: Path,
        width: int = DEFAULT_IMAGE_WIDTH,
        height: int = DEFAULT_IMAGE_HEIGHT
    ) -> Tuple[bool, Optional[str]]:
        valid, msg = self.validate_credentials()
        if not valid:
            return False, msg

        endpoint = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # DALL-E 3 supports 1024x1024 square images
        payload = {
            "model": self.model,
            "prompt": prompt.image_prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(endpoint, data=req_data, headers=headers, method="POST")
            
            with urllib.request.urlopen(req, timeout=90) as response:
                res_json = json.loads(response.read().decode("utf-8"))
                
                b64_data = res_json["data"][0].get("b64_json")
                if not b64_data:
                    url = res_json["data"][0].get("url")
                    if not url:
                        return False, "No image data or URL in OpenAI response."
                    urllib.request.urlretrieve(url, output_path)
                else:
                    img_bytes = base64.b64decode(b64_data)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)

            # Ensure square 1080x1080 dimensions
            with Image.open(output_path) as im:
                if im.size != (width, height):
                    resized = im.resize((width, height), Image.Resampling.LANCZOS)
                    resized.save(output_path, "PNG")

            return True, None

        except urllib.error.HTTPError as e:
            try:
                err_body = json.loads(e.read().decode("utf-8"))
                err_msg = err_body.get("error", {}).get("message", e.reason)
            except Exception:
                err_msg = e.reason
            return False, f"OpenAI API HTTP {e.code}: {err_msg}"
        except Exception as e:
            return False, f"OpenAI generation failed: {str(e)}"


class StabilityAIProvider(BaseProvider):
    """
    Stability AI Image Generation Provider (Stable Image Core / SD3).
    Requires STABILITY_API_KEY environment variable.
    """
    name = "stability"

    def __init__(self):
        self.api_key = get_env_var("STABILITY_API_KEY")

    def validate_credentials(self) -> Tuple[bool, str]:
        if not self.api_key:
            return False, "Missing STABILITY_API_KEY in environment or .env."
        return True, "Stability AI credentials configured."

    def get_cost_info(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "cost_per_image_usd": 0.030,
            "estimated_30_batch_cost_usd": 0.90,
            "quota_limit": "Consumes credits on cloud.stability.ai",
            "notes": "Outputs 1:1 aspect ratio square image."
        }

    def generate(
        self,
        prompt: FlyerPrompt,
        output_path: Path,
        width: int = DEFAULT_IMAGE_WIDTH,
        height: int = DEFAULT_IMAGE_HEIGHT
    ) -> Tuple[bool, Optional[str]]:
        valid, msg = self.validate_credentials()
        if not valid:
            return False, msg

        endpoint = "https://api.stability.ai/v2beta/stable-image/generate/core"
        
        # Build multipart/form-data
        boundary = "----StabilityFormBoundary" + hex(int(time.time()))[2:]
        lines = []
        fields = {
            "prompt": prompt.image_prompt,
            "output_format": "png",
            "aspect_ratio": "1:1"
        }
        
        body_parts = []
        for k, v in fields.items():
            body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode("utf-8"))
        body_parts.append(f"--{boundary}--\r\n".encode("utf-8"))
        body_data = b"".join(body_parts)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }

        try:
            req = urllib.request.Request(endpoint, data=body_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=90) as resp:
                img_data = resp.read()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_data)

            # Ensure 1080x1080
            with Image.open(output_path) as im:
                if im.size != (width, height):
                    resized = im.resize((width, height), Image.Resampling.LANCZOS)
                    resized.save(output_path, "PNG")

            return True, None

        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")
            except Exception:
                err_body = str(e.reason)
            return False, f"Stability API HTTP {e.code}: {err_body}"
        except Exception as e:
            return False, f"Stability AI generation error: {str(e)}"


class GoogleImagenProvider(BaseProvider):
    """
    Google Imagen / Gemini Image Provider.
    Requires GEMINI_API_KEY or GOOGLE_API_KEY environment variable.
    """
    name = "imagen"

    def __init__(self):
        self.api_key = get_env_var("GEMINI_API_KEY") or get_env_var("GOOGLE_API_KEY")

    def validate_credentials(self) -> Tuple[bool, str]:
        if not self.api_key:
            return False, "Missing GEMINI_API_KEY or GOOGLE_API_KEY in environment or .env."
        return True, "Google Imagen credentials configured."

    def get_cost_info(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "cost_per_image_usd": 0.030,
            "estimated_30_batch_cost_usd": 0.90,
            "quota_limit": "Google AI Studio quota / billing",
            "notes": "Uses Google Imagen 3 generate images endpoint."
        }

    def generate(
        self,
        prompt: FlyerPrompt,
        output_path: Path,
        width: int = DEFAULT_IMAGE_WIDTH,
        height: int = DEFAULT_IMAGE_HEIGHT
    ) -> Tuple[bool, Optional[str]]:
        valid, msg = self.validate_credentials()
        if not valid:
            return False, msg

        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "instances": [{"prompt": prompt.image_prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "1:1",
                "outputMimeType": "image/png"
            }
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(endpoint, data=req_data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=90) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                predictions = res.get("predictions", [])
                if not predictions or "bytesBase64Encoded" not in predictions[0]:
                    return False, f"Unexpected response from Google Imagen: {res}"
                img_bytes = base64.b64decode(predictions[0]["bytesBase64Encoded"])
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_bytes)

            with Image.open(output_path) as im:
                if im.size != (width, height):
                    resized = im.resize((width, height), Image.Resampling.LANCZOS)
                    resized.save(output_path, "PNG")
            return True, None

        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")
            except Exception:
                err_body = str(e.reason)
            return False, f"Google Imagen API HTTP {e.code}: {err_body}"
        except Exception as e:
            return False, f"Google Imagen generation failed: {str(e)}"


class MockProvider(BaseProvider):
    """
    Mock Provider for automated test suites.
    Instantly creates a mock 1080x1080 image without network overhead.
    """
    name = "mock"

    def validate_credentials(self) -> Tuple[bool, str]:
        return True, "Mock provider is always ready."

    def get_cost_info(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "cost_per_image_usd": 0.0,
            "estimated_30_batch_cost_usd": 0.0,
            "notes": "Testing mock only. No API calls made."
        }

    def generate(
        self,
        prompt: FlyerPrompt,
        output_path: Path,
        width: int = DEFAULT_IMAGE_WIDTH,
        height: int = DEFAULT_IMAGE_HEIGHT
    ) -> Tuple[bool, Optional[str]]:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            im = Image.new("RGB", (width, height), color=(108, 43, 217))
            draw = ImageDraw.Draw(im)
            draw.text((50, 50), f"MOCK: {prompt.id} - {prompt.title}", fill=(255, 255, 255))
            im.save(output_path, "PNG")
            return True, None
        except Exception as e:
            return False, str(e)


# Registry of available providers
PROVIDER_REGISTRY = {
    "local": LocalBrandedProvider,
    "openai": OpenAIProvider,
    "stability": StabilityAIProvider,
    "imagen": GoogleImagenProvider,
    "mock": MockProvider
}

def get_provider(name: Optional[str] = None) -> BaseProvider:
    """Instantiate and return provider adapter."""
    p_name = (name or get_env_var("FLYER_PROVIDER", "local")).lower().strip()
    provider_cls = PROVIDER_REGISTRY.get(p_name)
    if not provider_cls:
        available = ", ".join(PROVIDER_REGISTRY.keys())
        raise ValueError(f"Unknown provider '{p_name}'. Available providers: {available}")
    return provider_cls()
