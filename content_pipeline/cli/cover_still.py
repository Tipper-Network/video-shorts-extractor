#!/usr/bin/env python3
"""Write one cover still from the signed cut at the land clock."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def land_offset(segments: list[dict]) -> float:
    """Seconds into the rendered cut where the land is spoken.

    Segment clocks are source time. The cut plays them back to back.
    """
    elapsed = 0.0
    found: float | None = None
    for seg in segments:
        start = float(seg["start"])
        end = float(seg["end"])
        dur = max(0.0, end - start)
        label = str(seg.get("label") or "").lower()
        if any(key in label for key in ("resol", "land", "close")):
            found = elapsed + min(0.4, dur * 0.2)
        elapsed += dur
    if found is None:
        found = max(0.0, elapsed * 0.85)
    return found


def _mean_luma(image: Path) -> float:
    probe = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-i", str(image),
            "-f", "rawvideo", "-pix_fmt", "gray", "-",
        ],
        capture_output=True,
        check=False,
    )
    data = probe.stdout
    if not data:
        return 0.0
    return sum(data) / len(data)


def grab_frame(video: Path, at: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-ss", f"{at:.3f}", "-i", str(video),
            "-frames:v", "1", "-q:v", "2", str(dest),
        ],
        capture_output=True,
        check=True,
    )


def write_cover(video: Path, dest: Path, at: float) -> Path:
    """Grab one frame. If it is black, step forward until a real frame lands."""
    attempt = max(0.0, at)
    last = dest
    for _ in range(4):
        grab_frame(video, attempt, dest)
        if dest.exists() and dest.stat().st_size > 4000 and _mean_luma(dest) >= 16:
            print(f" Cover {attempt:.2f}s → {dest}")
            return dest
        attempt += 0.5
        last = dest
    raise SystemExit(f"No usable cover frame in {video} near {at:.2f}s (last {last})")


def segments_for_stem(short: dict, stem: str) -> list[dict]:
    versions = short.get("versions") or [short]
    chosen = versions[0]
    for version in versions:
        vid = str(version.get("version_id") or "")
        if vid and vid in stem:
            chosen = version
            break
    return list(chosen.get("segments") or short.get("segments") or [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Cover still at the land clock")
    parser.add_argument("--input", required=True, type=Path, help="Signed cut mp4")
    parser.add_argument("--output", required=True, type=Path, help="viral/covers/{stem}.jpg")
    parser.add_argument("--at", type=float, help="Seconds into the cut. Default: near the end")
    args = parser.parse_args()
    if not args.input.exists():
        raise SystemExit(f"Missing cut: {args.input}")
    at = args.at if args.at is not None else 1.0
    write_cover(args.input, args.output, at)


if __name__ == "__main__":
    main()
