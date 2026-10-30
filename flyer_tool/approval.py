"""
Ameetech Bulk Flyer Generation Tool
Approval Workflow Manager.
Strictly ensures no image is automatically copied to approved/ without explicit user action.
"""
from pathlib import Path
import shutil
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

from flyer_tool.config import (
    GENERATED_DIR,
    APPROVED_DIR,
    FAILED_DIR,
    DEFAULT_PROMPTS_JSON,
    DEFAULT_PROMPTS_CSV
)
from flyer_tool.models import FlyerPrompt, load_prompts_file, save_prompts_file
from flyer_tool.gallery import generate_preview_gallery

def approve_flyer(
    identifier: str,
    prompts_file: Path = DEFAULT_PROMPTS_JSON
) -> Tuple[bool, str]:
    """
    Approve a flyer by ID or filename.
    Copies image from generated/ to approved/ and updates prompt status.
    """
    prompts = load_prompts_file(prompts_file)
    target_prompt: Optional[FlyerPrompt] = None

    for p in prompts:
        if p.id.lower() == identifier.lower() or p.filename.lower() == identifier.lower():
            target_prompt = p
            break

    if not target_prompt:
        return False, f"No flyer found matching ID or filename: '{identifier}'"

    source_path = GENERATED_DIR / target_prompt.filename
    if not source_path.exists():
        # Check if already in approved/
        dest_path = APPROVED_DIR / target_prompt.filename
        if dest_path.exists():
            target_prompt.status = "approved"
            save_prompts_file(prompts, prompts_file)
            if prompts_file == DEFAULT_PROMPTS_JSON and DEFAULT_PROMPTS_CSV.exists():
                save_prompts_file(prompts, DEFAULT_PROMPTS_CSV)
            elif prompts_file == DEFAULT_PROMPTS_CSV and DEFAULT_PROMPTS_JSON.exists():
                save_prompts_file(prompts, DEFAULT_PROMPTS_JSON)
            generate_preview_gallery(prompts)
            return True, f"Flyer {target_prompt.id} is already approved and present in {dest_path.name}."
        return False, f"Image for {target_prompt.id} has not been generated yet (missing {source_path})."

    # Copy to approved/
    APPROVED_DIR.mkdir(parents=True, exist_ok=True)
    dest_path = APPROVED_DIR / target_prompt.filename
    shutil.copy2(source_path, dest_path)

    # Update status
    target_prompt.status = "approved"
    save_prompts_file(prompts, prompts_file)
    if prompts_file == DEFAULT_PROMPTS_JSON and DEFAULT_PROMPTS_CSV.exists():
        save_prompts_file(prompts, DEFAULT_PROMPTS_CSV)
    elif prompts_file == DEFAULT_PROMPTS_CSV and DEFAULT_PROMPTS_JSON.exists():
        save_prompts_file(prompts, DEFAULT_PROMPTS_JSON)

    generate_preview_gallery(prompts)
    return True, f"Successfully approved {target_prompt.id} ({target_prompt.filename}) -> copied to approved/"


def approve_all(prompts_file: Path = DEFAULT_PROMPTS_JSON) -> Tuple[int, int, List[str]]:
    """
    Approve all successfully generated flyers that are not yet approved.
    Returns: (approved_count: int, skipped_count: int, messages: List[str])
    """
    prompts = load_prompts_file(prompts_file)
    APPROVED_DIR.mkdir(parents=True, exist_ok=True)
    
    approved_count = 0
    skipped_count = 0
    messages = []

    for p in prompts:
        source_path = GENERATED_DIR / p.filename
        dest_path = APPROVED_DIR / p.filename

        if dest_path.exists():
            if p.status != "approved":
                p.status = "approved"
            skipped_count += 1
            messages.append(f"{p.id}: already in approved/")
            continue

        if source_path.exists():
            shutil.copy2(source_path, dest_path)
            p.status = "approved"
            approved_count += 1
            messages.append(f"{p.id}: approved -> {p.filename}")
        else:
            skipped_count += 1
            messages.append(f"{p.id}: skipped (not yet generated)")

    save_prompts_file(prompts, prompts_file)
    if prompts_file == DEFAULT_PROMPTS_JSON and DEFAULT_PROMPTS_CSV.exists():
        save_prompts_file(prompts, DEFAULT_PROMPTS_CSV)
    elif prompts_file == DEFAULT_PROMPTS_CSV and DEFAULT_PROMPTS_JSON.exists():
        save_prompts_file(prompts, DEFAULT_PROMPTS_JSON)

    generate_preview_gallery(prompts)
    return approved_count, skipped_count, messages


def reject_flyer(
    identifier: str,
    reason: str = "Quality review rejected",
    prompts_file: Path = DEFAULT_PROMPTS_JSON
) -> Tuple[bool, str]:
    """Move flyer to failed/ and update status."""
    prompts = load_prompts_file(prompts_file)
    target_prompt = None

    for p in prompts:
        if p.id.lower() == identifier.lower() or p.filename.lower() == identifier.lower():
            target_prompt = p
            break

    if not target_prompt:
        return False, f"No flyer found matching ID or filename: '{identifier}'"

    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    source_path = GENERATED_DIR / target_prompt.filename
    if source_path.exists():
        dest_path = FAILED_DIR / target_prompt.filename
        shutil.move(str(source_path), str(dest_path))

    target_prompt.status = "failed"
    save_prompts_file(prompts, prompts_file)
    if prompts_file == DEFAULT_PROMPTS_JSON and DEFAULT_PROMPTS_CSV.exists():
        save_prompts_file(prompts, DEFAULT_PROMPTS_CSV)
    elif prompts_file == DEFAULT_PROMPTS_CSV and DEFAULT_PROMPTS_JSON.exists():
        save_prompts_file(prompts, DEFAULT_PROMPTS_JSON)

    generate_preview_gallery(prompts)
    return True, f"Marked {target_prompt.id} as failed/rejected (Reason: {reason})."
