#!/usr/bin/env python3
"""Trim dead air from video — wraps auto-editor or ffmpeg silenceremove."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def trim_with_auto_editor(input_path: Path, output_path: Path, margin: str) -> None:
    ae = shutil.which("auto-editor")
    if not ae:
        print(" auto-editor not found in PATH")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ae,
        str(input_path),
        "--output", str(output_path),
        "--edit", "audio",
        "--margin", margin,
        "--no-open",
    ]
    print(f" Running: {' '.join(cmd)}", flush=True)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def trim_long_pauses_ffmpeg(
    input_path: Path,
    output_path: Path,
    min_silence: float,
    threshold_db: float,
) -> None:
    """Remove audio silence >= min_silence seconds (keeps A/V in sync via re-encode)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    af = (
        f"silenceremove=stop_periods=-1:stop_duration={min_silence}"
        f":stop_threshold={threshold_db}dB:detection=peak"
    )
    cmd = [
        "ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "warning",
        "-i", str(input_path),
        "-af", af,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(output_path),
    ]
    print(f" Removing silences >= {min_silence}s (threshold {threshold_db}dB)...", flush=True)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Trim dead air from video")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--method",
        choices=["auto-editor", "ffmpeg"],
        default="auto-editor",
        help="auto-editor=general silence; ffmpeg=long pauses only",
    )
    parser.add_argument("--margin", default="0.25sec", help="auto-editor margin")
    parser.add_argument(
        "--min-silence",
        type=float,
        default=10.0,
        help="ffmpeg: only remove pauses this long or longer (seconds)",
    )
    parser.add_argument("--threshold", type=float, default=-40.0, help="Silence threshold dB")
    parser.add_argument("--project", help="Project ID for timing log (e.g. hikmat)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        print(f" Not found: {input_path}")
        sys.exit(1)

    before = probe_duration(input_path)
    print(f" Input: {input_path.name} ({before:.1f}s)", flush=True)

    from contextlib import nullcontext

    timer_ctx = nullcontext()
    if args.project:
        from pipeline_log import StageTimer
        timer_ctx = StageTimer(
            args.project,
            "trim_silence",
            message=f"method={args.method}",
            artifact=str(output_path),
        )

    with timer_ctx:
        if args.method == "auto-editor":
            trim_with_auto_editor(input_path, output_path, args.margin)
        else:
            trim_long_pauses_ffmpeg(input_path, output_path, args.min_silence, args.threshold)

    after = probe_duration(output_path)
    saved = before - after
    print(f" Output: {output_path} ({after:.1f}s, removed ~{saved:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
