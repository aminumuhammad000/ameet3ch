"""
Ameetech Bulk Flyer Generation Tool
Configuration and constants.
"""
import os
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT_DIR / "prompts"
GENERATED_DIR = ROOT_DIR / "generated"
APPROVED_DIR = ROOT_DIR / "approved"
FAILED_DIR = ROOT_DIR / "failed"

DEFAULT_PROMPTS_JSON = PROMPTS_DIR / "flyer-prompts.json"
DEFAULT_PROMPTS_CSV = PROMPTS_DIR / "flyer-prompts.csv"
DEFAULT_REPORT_JSON = GENERATED_DIR / "generation_report.json"
DEFAULT_REPORT_MD = GENERATED_DIR / "generation_report.md"
GALLERY_HTML = ROOT_DIR / "preview_gallery.html"
GENERATED_GALLERY_HTML = GENERATED_DIR / "index.html"

# Primary Ameetech Logo candidates
LOGO_CANDIDATES = [
    ROOT_DIR / "images" / "ameelogo.png",
    ROOT_DIR / "images" / "ameelogo2.png",
    ROOT_DIR / "aminu-portfolio" / "ameelogo.png"
]

def get_logo_path() -> Path:
    for candidate in LOGO_CANDIDATES:
        if candidate.exists():
            return candidate
    return LOGO_CANDIDATES[0]

# Ameetech Brand Standards
BRAND_NAME = "Ameetech"
BRAND_FULL_NAME = "Amee Technology Ltd"
BRAND_TAGLINE = "Modern Enterprise Engineering & Digital Automation"
BRAND_WEBSITE = "ameetechnology.com.ng"
BRAND_WHATSAPP = "+234 810 001 5498"

# Brand Palette (from style.css)
COLOR_PRIMARY = "#6C2BD9"        # Ameetech Purple (RGB: 108, 43, 217)
COLOR_PRIMARY_DARK = "#581CBA"   # Secondary / Hover Purple (RGB: 88, 28, 186)
COLOR_ACCENT_TINT = "#F3E8FF"    # Soft Lavender Tint (RGB: 243, 232, 255)
COLOR_ACCENT_PINK = "#FF82A9"    # Accent Coral Pink (RGB: 255, 130, 169)
COLOR_BG_WHITE = "#FFFFFF"       # Crisp White (RGB: 255, 255, 255)
COLOR_BG_LIGHT = "#F8FAFC"       # Slate 50 (RGB: 248, 250, 252)
COLOR_TEXT_MAIN = "#1E1B4B"      # Deep Navy/Charcoal (RGB: 30, 27, 75)
COLOR_TEXT_MUTED = "#64748B"     # Slate 500 (RGB: 100, 116, 139)
COLOR_BORDER = "#E2E8F0"         # Slate 200 (RGB: 226, 232, 240)

# Image Dimensions
DEFAULT_IMAGE_WIDTH = 1080
DEFAULT_IMAGE_HEIGHT = 1080

def get_env_var(name: str, default: str = "") -> str:
    """Read environment variable or check local .env file if available."""
    val = os.environ.get(name)
    if val is not None:
        return val.strip()
    
    # Check .env file in root
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") or not line or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    if k.strip() == name:
                        # strip comments and quotes
                        v = v.split("#")[0].strip().strip('"').strip("'")
                        return v
        except Exception:
            pass
    return default

def get_provider_name() -> str:
    return get_env_var("FLYER_PROVIDER", "local").lower()

def get_concurrency() -> int:
    try:
        return max(1, int(get_env_var("FLYER_CONCURRENCY", "2")))
    except ValueError:
        return 2

def get_max_retries() -> int:
    try:
        return max(0, int(get_env_var("FLYER_MAX_RETRIES", "3")))
    except ValueError:
        return 3

def get_batch_size() -> int:
    try:
        return max(1, int(get_env_var("FLYER_BATCH_SIZE", "10")))
    except ValueError:
        return 10
