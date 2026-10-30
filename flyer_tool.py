#!/usr/bin/env python3
"""
Ameetech Bulk Flyer Generation Tool
Executable entry point.
"""
import sys
from pathlib import Path

# Ensure root workspace is on python path
root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from flyer_tool.cli import main

if __name__ == "__main__":
    main()
