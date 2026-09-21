#!/usr/bin/env python3
"""
Run a single pipeline module for a project.

Each module is independently callable — compose them per project via
projects/{id}/pipeline.json + agent instructions.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODULES = {
    "concat": {
        "script": "concat_clips.py",
        "description": "Chronological multi-clip assembly",
    },
    "srt_to_text": {
        "script": "srt_to_text.py",
        "description": "YouTube SRT → titled plains in transcript root + optional clock files",
    },
    "detect_topics": {
        "script": "detect_topics.py",
        "description": "Heuristic topic blocks + chapter candidates from transcript",
    },
    "compose_shorts": {
        "script": "compose_shorts.py",
        "description": "Visual segment pool + montage manifest (timelapse projects)",
    },
    "render": {
        "script": "render_manifest.py",
        "description": "Batch render chapters + shorts from manifest",
    },
    "trim_silence": {
        "script": "trim_silence.py",
        "description": "Standalone silence trim on one file",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one pipeline module")
    parser.add_argument("--module", required=True, choices=sorted(MODULES.keys()))
    parser.add_argument("--project", help="Project ID — loads projects/{id}/pipeline.json")
    parser.add_argument("extra", nargs=argparse.REMAINDER, help="Args passed to the underlying script")
    args = parser.parse_args()

    if args.project:
        from project_config import module_enabled

        if not module_enabled(args.project, args.module):
            print(f" Module '{args.module}' is disabled for project '{args.project}'")
            print(" Enable it in projects/{project}/pipeline.json")
            sys.exit(1)

    info = MODULES[args.module]
    script = BASE_DIR / info["script"]
    cmd = [sys.executable, str(script), *info.get("fixed_args", []), *args.extra]

    if args.project and "--project" not in args.extra:
        # pass project to scripts that support it
        if args.module in ("concat", "trim_silence", "detect_topics", "render", "transcribe", "srt_to_text"):
            cmd.extend(["--project", args.project])

    if args.module == "transcribe" and args.project and "--input" not in args.extra:
        pass  # one video in input/: auto-detect. several: pass -- --input filename

    print(f" Module: {args.module} — {info['description']}")
    result = subprocess.run(cmd, cwd=BASE_DIR)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
