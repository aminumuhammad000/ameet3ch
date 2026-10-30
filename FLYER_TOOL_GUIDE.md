# Ameetech Bulk Flyer Generation & Approval Tool

A production-grade, modular automation tool designed to generate, review, and approve branded square (1080×1080) social media promotional flyers for **Amee Technology Ltd (Ameetech)**.

---

## 1. Ameetech Brand Identity & Guidelines

All flyers strictly adhere to the Ameetech visual brand standards:
- **Primary Brand Color**: `#6C2BD9` (Vibrant Ameetech Royal Purple)
- **Secondary / Accent Colors**: `#581CBA` (Deep Violet), `#F3E8FF` (Soft Lavender Tint), `#FF82A9` (Coral Pink Accent)
- **Background**: Crisp clean white (`#FFFFFF`) with restrained geometric gradients and subtle tech grid accents.
- **Typography**: Clean, high-contrast, modern sans-serif hierarchy optimized for mobile feeds.
- **Logo Asset**: Uses the transparent brand logo at [`images/ameelogo.png`](file:///home/ameetech/Desktop/ameet3ch/images/ameelogo.png).
- **Official Contact Footer**: 
  - 🌐 Website: `ameetechnology.com.ng`
  - 💬 WhatsApp: `+234 810 001 5498`
- **Authenticity Policy**: Promotes real Ameetech services without invented awards, fake metrics, or fabricated prices.

---

## 2. Directory Architecture

The tool automatically initializes and manages the required directories:

```
ameet3ch/
├── prompts/
│   ├── flyer-prompts.json           # 30 structured Ameetech flyer records (JSON)
│   └── flyer-prompts.csv            # 30 structured Ameetech flyer records (CSV)
├── generated/                       # Raw batch output from image providers
│   ├── ameetech-01-enterprise-web-apps.png
│   ├── ameetech-02-mobile-app-development.png
│   ├── ... (all 30 generated flyers)
│   ├── generation_report.json       # Structured generation metadata & duration
│   ├── generation_report.md         # Formatted generation markdown report
│   └── index.html                   # Embedded copy of review gallery
├── approved/                        # Final verified production assets
│   └── (Only populated when explicitly approved by the user!)
├── failed/                          # Rejected or errored flyer generations
├── flyer_tool/                      # Modular Python package
│   ├── __init__.py
│   ├── config.py                    # Environment, brand palette, paths
│   ├── models.py                    # FlyerPrompt dataclass & validation rules
│   ├── providers.py                 # Provider adapter implementations
│   ├── engine.py                    # Concurrent batch engine & retries
│   ├── gallery.py                   # Ameetech-branded HTML preview gallery
│   ├── approval.py                  # Human approval workflow manager
│   └── cli.py                       # CLI parsing and command dispatcher
├── flyer_tool.py                    # Root CLI executable
├── preview_gallery.html             # Standalone local HTML review gallery
└── test_flyer_tool.py               # Comprehensive unit and integration test suite
```

---

## 3. Supported Image Generation Providers

The tool uses a plug-and-play **Provider Adapter Pattern** configured via the `FLYER_PROVIDER` setting or CLI `--provider` flag:

| Provider | Adapter Name | Credentials | Estimated Cost (30 Flyers) | Output Specs |
|---|---|---|---|---|
| **Local Branded Compositor** *(Default)* | `local` | None (Local Pillow) | **$0.00** (Free, Offline) | 1080×1080 PNG with logo & brand footer |
| **OpenAI DALL-E 3** | `openai` | `OPENAI_API_KEY` | ~$1.20 ($0.040/flyer) | 1024×1024 resized to 1080×1080 |
| **Stability AI Core / SD3** | `stability` | `STABILITY_API_KEY` | ~$0.90 ($0.030/flyer) | 1:1 square PNG resized to 1080×1080 |
| **Google Imagen 3** | `imagen` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | ~$0.90 ($0.030/flyer) | 1:1 square PNG resized to 1080×1080 |
| **Mock Provider** | `mock` | None | **$0.00** | Test stub for headless CI pipelines |

---

## 4. Setup & Environment Configuration

### Dependencies
The tool requires Python 3.10+ with standard packages:
- `Pillow` (already installed in your environment: `12.1.1`)
- Standard library modules: `urllib`, `concurrent.futures`, `json`, `csv`, `pathlib`, `argparse`.

### Environment Variables
Copy `.env.example` to `.env` (or configure your shell environment):
```bash
# Set your desired active provider
export FLYER_PROVIDER=local

# Concurrency and batching
export FLYER_CONCURRENCY=2
export FLYER_BATCH_SIZE=10
export FLYER_MAX_RETRIES=3

# External Provider API Keys (optional if using 'local')
export OPENAI_API_KEY="sk-..."
export STABILITY_API_KEY="sk-..."
export GEMINI_API_KEY="..."
```

---

## 5. Command Reference

### A. Dry-Run Validation (Zero Cost / Safe Inspection)
Validates all 30 prompt records, verifies unique filenames, checks directory readiness, tests provider credentials, and displays estimated costs without spending API credits:
```bash
python3 flyer_tool.py dry-run
```
To dry-run test a specific cloud provider:
```bash
python3 flyer_tool.py dry-run --provider openai
python3 flyer_tool.py dry-run --provider stability
```

### B. Validate Prompts & Filesystem
Validates syntax, schemas, and filename safety rules:
```bash
python3 flyer_tool.py validate
```

### C. Run Batch Generation
Process all 30 flyers with progress reporting, concurrency control, and automatic retry handling:
```bash
python3 flyer_tool.py generate --provider local
```
**Flags**:
- `--concurrency 2`: Controls simultaneous generation threads (avoids rate limits).
- `--batch-size 10`: Processes flyers in discrete batches.
- `--force`: Regenerates flyers even if already present in `generated/`.
- `--id FLYER-005`: Generates or re-runs a single specific flyer.

### D. Status Overview
View an ASCII table showing the status of each flyer in `generated/` and `approved/`:
```bash
python3 flyer_tool.py status
```

### E. Interactive Preview & Review Gallery
Generates and displays the path to the Ameetech local HTML dashboard:
```bash
python3 flyer_tool.py review
```
Open `preview_gallery.html` in your web browser:
- Filter by status (**All**, **Generated**, **Approved**, **Pending**, **Failed**).
- Fullscreen zoom and card preview for mobile rendering.
- Copy filenames or approval CLI commands with 1-click.
- Interactive Approval Center.

### F. Approval Workflow (Publishing Safeguard)
As required, **no generated image is automatically copied to `approved/`**. You must explicitly approve:

**Approve a single flyer**:
```bash
python3 flyer_tool.py approve FLYER-001
```

**Approve all generated flyers**:
```bash
python3 flyer_tool.py approve --all
```

**Reject a flyer with a review note**:
```bash
python3 flyer_tool.py reject FLYER-004 --reason "Text placement needs adjustment"
```

---

## 6. Running the Test Suite

Run the flyer tool test suite:
```bash
python3 -m unittest test_flyer_tool.py
```

Run all project tests across the entire repository (67 tests):
```bash
python3 -m unittest discover -p "test_*.py"
```
