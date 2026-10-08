"""Pipeline filesystem roots — import after putting this package root on sys.path."""

from __future__ import annotations

from pathlib import Path

PIPELINE_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = PIPELINE_ROOT.parent
CONFIG_DIR = PIPELINE_ROOT / "config"
LIB_DIR = PIPELINE_ROOT / "lib"
CLI_DIR = PIPELINE_ROOT / "cli"


def ensure_import_path() -> None:
    """Put ``lib/`` and ``cli/`` on ``sys.path`` so flat imports keep working."""
    import sys

    for path in (LIB_DIR, CLI_DIR, PIPELINE_ROOT):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)
