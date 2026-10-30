"""
Ameetech Bulk Flyer Generation Tool
Command-Line Interface (CLI).
"""
import argparse
import sys
from pathlib import Path
import json

from flyer_tool.config import (
    ROOT_DIR,
    DEFAULT_PROMPTS_JSON,
    DEFAULT_PROMPTS_CSV,
    GENERATED_DIR,
    APPROVED_DIR,
    FAILED_DIR,
    GALLERY_HTML
)
from flyer_tool.models import load_prompts_file
from flyer_tool.engine import FlyerEngine
from flyer_tool.approval import approve_flyer, approve_all, reject_flyer
from flyer_tool.gallery import generate_preview_gallery
from flyer_tool.providers import PROVIDER_REGISTRY

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flyer_tool",
        description="Ameetech Bulk Flyer Generation & Approval Tool"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    # generate / run
    gen_parser = subparsers.add_parser("generate", aliases=["run"], help="Generate flyers in batch")
    gen_parser.add_argument("--provider", "-p", choices=list(PROVIDER_REGISTRY.keys()), default=None,
                            help="Image generation provider (local, openai, stability, imagen, mock)")
    gen_parser.add_argument("--batch-size", "-b", type=int, default=None, help="Batch size (default: 10)")
    gen_parser.add_argument("--concurrency", "-c", type=int, default=None, help="Concurrency worker count (default: 2)")
    gen_parser.add_argument("--dry-run", "-d", action="store_true", help="Validate without generating or spending credits")
    gen_parser.add_argument("--force", "-f", action="store_true", help="Force regeneration even if file exists")
    gen_parser.add_argument("--id", type=str, default=None, help="Process single flyer ID or filename")
    gen_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON, help="Path to prompts JSON or CSV")

    # dry-run
    dry_parser = subparsers.add_parser("dry-run", help="Dry run validation")
    dry_parser.add_argument("--provider", "-p", choices=list(PROVIDER_REGISTRY.keys()), default=None)
    dry_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON)

    # validate
    val_parser = subparsers.add_parser("validate", help="Validate prompts and filesystem integrity")
    val_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON)

    # approve
    app_parser = subparsers.add_parser("approve", help="Approve flyer(s) and copy to approved/")
    app_parser.add_argument("identifier", nargs="?", default=None, help="Flyer ID or filename to approve")
    app_parser.add_argument("--all", "-a", action="store_true", help="Approve all generated flyers")
    app_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON)

    # reject
    rej_parser = subparsers.add_parser("reject", help="Reject a flyer and move to failed/")
    rej_parser.add_argument("identifier", help="Flyer ID or filename to reject")
    rej_parser.add_argument("--reason", "-r", default="Quality review rejected", help="Rejection reason")
    rej_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON)

    # review / gallery
    rev_parser = subparsers.add_parser("review", aliases=["gallery"], help="Build and view the local HTML review gallery")
    rev_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON)

    # status
    stat_parser = subparsers.add_parser("status", help="Display overview of all 30 flyers")
    stat_parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS_JSON)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    engine = FlyerEngine()

    if args.subcommand in ("generate", "run"):
        try:
            report = engine.process_batch(
                prompts_file=args.prompts,
                provider_name=args.provider,
                batch_size=args.batch_size,
                concurrency=args.concurrency,
                force=args.force,
                dry_run=args.dry_run,
                specific_id=args.id
            )
            if args.dry_run:
                _print_dry_run_summary(report)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    elif args.subcommand == "dry-run":
        report = engine.dry_run(args.prompts, args.provider)
        _print_dry_run_summary(report)
        if not report["success"]:
            sys.exit(1)

    elif args.subcommand == "validate":
        try:
            prompts = load_prompts_file(args.prompts)
            valid, errors = engine.validate_prompts(prompts)
            if valid:
                print(f"✅ Prompts file '{args.prompts}' is valid! ({len(prompts)} prompts inspected, 0 errors).")
            else:
                print(f"❌ Prompts file '{args.prompts}' contains {len(errors)} error(s):")
                for err in errors:
                    print(f"   - {err}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Failed to load prompts: {str(e)}", file=sys.stderr)
            sys.exit(1)

    elif args.subcommand == "approve":
        if args.all:
            count, skipped, msgs = approve_all(args.prompts)
            print(f"\n✅ Approved {count} generated flyers into 'approved/' (skipped {skipped}).")
            for m in msgs:
                print(f"   • {m}")
        elif args.identifier:
            ok, msg = approve_flyer(args.identifier, args.prompts)
            if ok:
                print(f"✅ {msg}")
            else:
                print(f"❌ {msg}", file=sys.stderr)
                sys.exit(1)
        else:
            print("❌ Must provide a flyer ID / filename or specify --all.", file=sys.stderr)
            sys.exit(1)

    elif args.subcommand == "reject":
        ok, msg = reject_flyer(args.identifier, args.reason, args.prompts)
        if ok:
            print(f"⚠️ {msg}")
        else:
            print(f"❌ {msg}", file=sys.stderr)
            sys.exit(1)

    elif args.subcommand in ("review", "gallery"):
        try:
            prompts = load_prompts_file(args.prompts)
            gallery_path = generate_preview_gallery(prompts)
            print(f"\n🎨 Preview Gallery Generated Successfully!")
            print(f"   Local file path: {gallery_path}")
            print(f"   Browser URL:     file://{gallery_path.resolve()}\n")
        except Exception as e:
            print(f"❌ Failed to generate gallery: {str(e)}", file=sys.stderr)
            sys.exit(1)

    elif args.subcommand == "status":
        _print_status_table(args.prompts)


def _print_dry_run_summary(report: Dict[str, Any]):
    print("\n" + "=" * 60)
    print("      AMEETECH BULK FLYER GENERATOR — DRY RUN REPORT      ")
    print("=" * 60)
    status_icon = "✅ READY" if report["success"] else "⚠️ ATTENTION NEEDED"
    print(f"Overall Status:        {status_icon}")
    print(f"Configured Provider:   {report['provider']}")
    print(f"Provider Credentials:  {'VALID' if report['provider_credentials_ok'] else 'INVALID / NOT FOUND'}")
    print(f"Provider Message:      {report['provider_status_message']}")
    print("-" * 60)
    print(f"Total Prompts:         {report['total_prompts']}")
    print(f"Pending Generation:    {report['pending_count']}")
    print(f"Already Generated:     {report['already_generated_count']}")
    print(f"Already Approved:      {report['already_approved_count']}")
    print("-" * 60)
    cost = report.get("cost_info", {})
    print(f"Cost Estimate per Img: ${cost.get('cost_per_image_usd', 0.0):.3f}")
    print(f"Estimated 30-Img Cost: ${cost.get('estimated_30_batch_cost_usd', 0.0):.2f}")
    print(f"Quota Limitations:     {cost.get('quota_limit', 'N/A')}")
    print(f"Provider Notes:        {cost.get('notes', 'N/A')}")
    print("-" * 60)
    print("Directories:")
    for name, path in report["directories_ready"].items():
        print(f"  • {name.ljust(10)}: {path}")

    if report.get("validation_errors"):
        print("\nValidation Errors:")
        for err in report["validation_errors"]:
            print(f"  ❌ {err}")
    print("=" * 60 + "\n")


def _print_status_table(prompts_file: Path):
    try:
        prompts = load_prompts_file(prompts_file)
    except Exception as e:
        print(f"❌ Error loading prompts: {str(e)}")
        return

    print("\n" + "=" * 80)
    print(f" AMEETECH FLYER COLLECTION STATUS ({len(prompts)} Prompts)")
    print("=" * 80)
    print(f"{'ID':<11} {'Status':<11} {'Generated':<11} {'Approved':<10} {'Filename':<35}")
    print("-" * 80)

    gen_count = 0
    app_count = 0

    for p in prompts:
        gen_exists = (GENERATED_DIR / p.filename).exists()
        app_exists = (APPROVED_DIR / p.filename).exists()
        if gen_exists: gen_count += 1
        if app_exists: app_count += 1
        
        status_str = "APPROVED" if app_exists else ("GENERATED" if gen_exists else p.status.upper())
        print(f"{p.id:<11} {status_str:<11} {'YES' if gen_exists else 'NO':<11} {'YES' if app_exists else 'NO':<10} {p.filename:<35}")

    print("-" * 80)
    print(f"Summary: Generated={gen_count}/{len(prompts)}, Approved={app_count}/{len(prompts)}")
    print("=" * 80 + "\n")
