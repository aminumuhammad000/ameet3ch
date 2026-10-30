"""
Ameetech Bulk Flyer Generation Tool
Data models and input validation.
"""
from dataclasses import dataclass, asdict, field
from pathlib import Path
import re
from typing import List, Dict, Any, Optional
import json
import csv

VALID_STATUSES = {"pending", "generated", "approved", "failed"}
SAFE_FILENAME_REGEX = re.compile(r"^[a-zA-Z0-9_\-\.]+\.(png|jpg|jpeg|webp)$", re.IGNORECASE)

@dataclass
class FlyerPrompt:
    id: str
    title: str
    filename: str
    image_prompt: str
    status: str = "pending"
    category: str = "General Tech"
    website: str = "ameetechnology.com.ng"
    whatsapp: str = "+234 810 001 5498"
    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> List[str]:
        """Validate prompt fields against requirements. Returns list of error messages."""
        errors = []
        if not self.id or not isinstance(self.id, str) or not self.id.strip():
            errors.append("Flyer ID must be a non-empty string.")
        
        if not self.title or not isinstance(self.title, str) or not self.title.strip():
            errors.append(f"Flyer {self.id}: Title must be a non-empty string.")
        
        if not self.filename or not isinstance(self.filename, str):
            errors.append(f"Flyer {self.id}: Filename must be specified.")
        else:
            fname = self.filename.strip()
            if "/" in fname or "\\" in fname or ".." in fname:
                errors.append(f"Flyer {self.id}: Filename contains invalid path separators: '{fname}'.")
            elif not SAFE_FILENAME_REGEX.match(fname):
                errors.append(
                    f"Flyer {self.id}: Filename '{fname}' is invalid. "
                    "Must end with .png, .jpg, .jpeg, or .webp and contain only alphanumeric, dash, or underscore characters."
                )

        if not self.image_prompt or not isinstance(self.image_prompt, str) or len(self.image_prompt.strip()) < 10:
            errors.append(f"Flyer {self.id}: Image prompt is missing or too short (must be >= 10 chars).")
        
        norm_status = (self.status or "pending").strip().lower()
        if norm_status not in VALID_STATUSES:
            errors.append(
                f"Flyer {self.id}: Invalid status '{self.status}'. Must be one of {sorted(VALID_STATUSES)}."
            )
        
        return errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "filename": self.filename,
            "image_prompt": self.image_prompt,
            "status": self.status,
            "website": self.website,
            "whatsapp": self.whatsapp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FlyerPrompt":
        return cls(
            id=str(data.get("id", "")).strip(),
            title=str(data.get("title", "")).strip(),
            category=str(data.get("category", "General Tech")).strip(),
            filename=str(data.get("filename", "")).strip(),
            image_prompt=str(data.get("image_prompt", "")).strip(),
            status=str(data.get("status", "pending")).strip().lower(),
            website=str(data.get("website", "ameetechnology.com.ng")).strip(),
            whatsapp=str(data.get("whatsapp", "+234 810 001 5498")).strip(),
            extra_metadata={k: v for k, v in data.items() if k not in {
                "id", "title", "category", "filename", "image_prompt", "status", "website", "whatsapp"
            }}
        )

@dataclass
class GenerationRecord:
    id: str
    filename: str
    status: str
    provider: str
    timestamp: str
    duration_seconds: float = 0.0
    error: Optional[str] = None
    output_path: Optional[str] = None
    width: int = 1080
    height: int = 1080
    retries_used: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def load_prompts_file(file_path: Path) -> List[FlyerPrompt]:
    """Load prompts from JSON or CSV. Preserves original prompt text."""
    if not file_path.exists():
        raise FileNotFoundError(f"Prompts file not found at: {file_path}")
    
    suffix = file_path.suffix.lower()
    prompts: List[FlyerPrompt] = []

    if suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON prompts file must contain a top-level list of prompt objects.")
            for item in data:
                prompts.append(FlyerPrompt.from_dict(item))
    elif suffix == ".csv":
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                prompts.append(FlyerPrompt.from_dict(row))
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Supported formats are .json and .csv.")
    
    return prompts

def save_prompts_file(prompts: List[FlyerPrompt], file_path: Path) -> None:
    """Save prompts list back to JSON or CSV."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = file_path.suffix.lower()
    
    if suffix == ".json":
        data = [p.to_dict() for p in prompts]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif suffix == ".csv":
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["id", "title", "category", "filename", "image_prompt", "status", "website", "whatsapp"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in prompts:
                writer.writerow(p.to_dict())
    else:
        raise ValueError(f"Unsupported file format '{suffix}' for saving prompts.")
