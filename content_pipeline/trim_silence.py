#!/usr/bin/env python3
"""Shim — real module: ``lib/trim_silence.py``."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(_ROOT / "lib"), str(_ROOT / "cli"), str(_ROOT)]
runpy.run_path(str(_ROOT / "lib" / "trim_silence.py"), run_name="__main__")
