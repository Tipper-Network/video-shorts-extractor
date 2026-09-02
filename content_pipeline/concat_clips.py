#!/usr/bin/env python3
"""Concatenate chronologically sorted clips into one timeline.

Modes:
  draft     — stream-copy first (~seconds). Falls back to one fast re-encode if needed.
  normalize — re-encode only clips that need it (portrait, missing audio, wrong size).
              Landscape clips with audio are stream-copied via intermediate TS segments.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

TIMESTAMP_RE = re.compile(r"^(\d{8})_(\d{6})")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
TARGET_W, TARGET_H = 1920, 1080
VF = (
    f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,"
    f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30"
)


@dataclass
class ClipInfo:
    path: Path
    width: int
    height: int
    has_audio: bool
    duration: float
    codec: str = "unknown"
    kind: str = "video"  # video | image

    @property
    def is_portrait(self) -> bool:
        return self.height > self.width

    @property
    def is_image(self) -> bool:
        return self.kind == "image"

    @property
    def needs_normalize(self) -> bool:
        if self.is_image:
            return True
        # HEVC/other codecs must re-encode — stream-copy concat breaks playback
        if self.codec not in ("h264", "avc1"):
            return True
        return (
            self.is_portrait
            or not self.has_audio
            or self.width != TARGET_W
            or self.height != TARGET_H
        )


def clip_sort_key(path: Path) -> tuple:
    match = TIMESTAMP_RE.match(path.stem)
    if match:
        return (match.group(1), match.group(2), path.name)
    return ("99999999", "999999", path.name)


def discover_clips(source_dir: Path, exclude: set[str], include_images: bool = False) -> list[Path]:
    items: list[Path] = []
    patterns = ["*.mp4"]
    if include_images:
        patterns.extend(["*.jpg", "*.jpeg", "*.png", "*.webp"])

    for pattern in patterns:
        for path in source_dir.glob(pattern):
            if path.name in exclude:
                continue
            if path.suffix.lower() == ".mp4" and path.stat().st_size < 100_000:
                continue
            items.append(path)

    return sorted(set(items), key=clip_sort_key)


def probe_image(path: Path, duration: float) -> ClipInfo:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    stream = json.loads(result.stdout)["streams"][0]
    return ClipInfo(
        path=path,
        width=int(stream["width"]),
        height=int(stream["height"]),
        has_audio=False,
        duration=duration,
        kind="image",
    )


def probe_clip(path: Path) -> ClipInfo:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,codec_name",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    stream = data["streams"][0]
    codec = stream.get("codec_name", "unknown")
    audio_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=index",
        "-of",
        "csv=p=0",
        str(path),
    ]
    has_audio = bool(
        subprocess.run(audio_cmd, capture_output=True, text=True).stdout.strip()
    )
    return ClipInfo(
        path=path,
        width=int(stream["width"]),
        height=int(stream["height"]),
        has_audio=has_audio,
        duration=float(data["format"]["duration"]),
        codec=codec,
        kind="video",
    )


def run_ffmpeg(cmd: list[str], label: str) -> None:
    print(f"  → {label}", flush=True)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"ffmpeg failed: {label}")


def concat_stream_copy(clips: list[Path], output_path: Path) -> bool:
    list_file = output_path.parent / "concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{clip.resolve()}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    list_file.unlink(missing_ok=True)
    if result.returncode != 0:
        print(f"  stream-copy failed: {result.stderr.strip()}", flush=True)
        return False
    return True


def concat_reencode(clips: list[Path], output_path: Path, preset: str) -> None:
    list_file = output_path.parent / "concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{clip.resolve()}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c:v",
        "libx264",
        "-preset",
        preset,
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    run_ffmpeg(cmd, f"re-encode concat ({preset})")
    list_file.unlink(missing_ok=True)


def image_to_video(info: ClipInfo, out_path: Path, preset: str) -> None:
    """Turn a still into a short 1080p segment with silent audio."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-loop",
        "1",
        "-i",
        str(info.path),
        "-f",
        "lavfi",
        "-i",
        "anullsrc=r=48000:cl=stereo",
        "-t",
        str(info.duration),
        "-vf",
        VF,
        "-c:v",
        "libx264",
        "-crf",
        "20",
        "-preset",
        preset,
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out_path),
    ]
    run_ffmpeg(cmd, f"image → video {info.path.name} ({info.duration:.1f}s)")


def normalize_clip(info: ClipInfo, out_path: Path, preset: str) -> None:
    if info.is_image:
        image_to_video(info, out_path, preset)
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    base = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-i",
        str(info.path),
    ]
    encode_tail = [
        "-vf",
        VF,
        "-c:v",
        "libx264",
        "-crf",
        "20",
        "-preset",
        preset,
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(out_path),
    ]
    if info.has_audio:
        run_ffmpeg(base + encode_tail, f"normalize {info.path.name}")
    else:
        run_ffmpeg(
            base
            + ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            + [
                "-vf", VF,
                "-c:v", "libx264", "-crf", "20", "-preset", preset,
                "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k",
                "-shortest",
                "-movflags", "+faststart",
                str(out_path),
            ],
            f"normalize {info.path.name} (+ silent audio)",
        )


def concat_draft(clips: list[Path], output_path: Path, preset: str) -> None:
    print("Mode: draft (stream-copy first)", flush=True)
    if concat_stream_copy(clips, output_path):
        print(" Used stream-copy — fast draft timeline.", flush=True)
        return
    print(" Falling back to single-pass re-encode...", flush=True)
    concat_reencode(clips, output_path, preset)


def concat_normalize(
    clip_infos: list[ClipInfo],
    output_path: Path,
    cache_dir: Path,
    preset: str,
    force: bool = False,
    reencode_all: bool = False,
) -> None:
    label = "full re-encode" if reencode_all else "normalize (as needed)"
    print(f"Mode: {label}", flush=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []

    for i, info in enumerate(clip_infos, 1):
        must_encode = reencode_all or info.needs_normalize
        seg = cache_dir / f"{info.path.stem}_norm.mp4"

        if must_encode:
            if force or not seg.exists():
                print(
                    f"[{i}/{len(clip_infos)}] encode {info.path.name} "
                    f"({info.width}x{info.height}, {info.codec}, "
                    f"audio={'yes' if info.has_audio else 'no'})",
                    flush=True,
                )
                normalize_clip(info, seg, preset)
            else:
                print(f"[{i}/{len(clip_infos)}] cache hit {seg.name}", flush=True)
            segments.append(seg)
        else:
            print(
                f"[{i}/{len(clip_infos)}] passthrough {info.path.name} ({info.codec})",
                flush=True,
            )
            segments.append(info.path)

    print(" Concatenating segments (re-encode for codec safety)...", flush=True)
    concat_reencode(segments, output_path, preset)


def print_summary(output_path: Path, clip_infos: list[ClipInfo]) -> None:
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size",
            "-of",
            "default=noprint_wrappers=1",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    total_src = sum(c.duration for c in clip_infos)
    print(probe.stdout.strip(), flush=True)
    print(
        f" Clips: {len(clip_infos)} | source total ~{total_src:.1f}s | "
        f"output: {output_path}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concat clips in chronological order (draft or normalize)"
    )
    parser.add_argument("--source-dir", required=True, help="Folder with raw MP4 clips")
    parser.add_argument("--output", help="Output MP4 path")
    parser.add_argument(
        "--series", default="assembly", help="Series name for default output folder"
    )
    parser.add_argument(
        "--exclude", nargs="*", default=["one.mp4"], help="Filenames to skip"
    )
    parser.add_argument(
        "--mode",
        choices=["draft", "normalize", "full"],
        default="draft",
        help="draft=stream-copy; normalize=encode clips that need it; full=re-encode ALL clips",
    )
    parser.add_argument(
        "--preset",
        default="ultrafast",
        help="x264 preset when re-encode is required (default: ultrafast for drafts)",
    )
    parser.add_argument(
        "--cache-dir",
        help="Normalized clip cache (default: <output_dir>/normalized)",
    )
    parser.add_argument(
        "--include-images",
        action="store_true",
        help="Include JPG/PNG/WebP in chronological order (converted to short video segments)",
    )
    parser.add_argument(
        "--image-duration",
        type=float,
        default=4.0,
        help="Seconds each still is held on screen (default: 4)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-encode cached segments even if they exist",
    )
    parser.add_argument(
        "--project",
        help="Project ID for pipeline stage log (e.g. hikmat)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print clip order and probe info only",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.is_dir():
        print(f" Not a directory: {source_dir}")
        sys.exit(1)

    exclude = set(args.exclude or [])
    clips = discover_clips(source_dir, exclude, include_images=args.include_images)
    if not clips:
        print(" No clips found.")
        sys.exit(1)

    clip_infos: list[ClipInfo] = []
    for path in clips:
        if path.suffix.lower() in IMAGE_EXTS:
            clip_infos.append(probe_image(path, args.image_duration))
        else:
            clip_infos.append(probe_clip(path))

    print(" Order:", flush=True)
    for i, info in enumerate(clip_infos, 1):
        flags = []
        if info.is_portrait:
            flags.append("portrait")
        if not info.has_audio:
            flags.append("no-audio")
        if info.codec not in ("h264", "avc1"):
            flags.append(info.codec)
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        kind = "still" if info.is_image else "video"
        print(
            f"  {i:2}. {info.path.name}  {info.duration:.1f}s  "
            f"{info.width}x{info.height}  [{kind}]{flag_str}",
            flush=True,
        )

    if args.dry_run:
        need = sum(1 for c in clip_infos if c.needs_normalize)
        print(f"\n normalize would re-encode {need}/{len(clip_infos)} clips", flush=True)
        return

    out_dir = OUTPUT_DIR / args.series
    output_path = (
        Path(args.output)
        if args.output
        else out_dir / f"{args.series}_timeline_{args.mode}.mp4"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir = (
        Path(args.cache_dir)
        if args.cache_dir
        else output_path.parent / "normalized"
    )

    from contextlib import nullcontext

    timer_ctx = nullcontext()
    if args.project:
        from pipeline_log import StageTimer
        timer_ctx = StageTimer(
            args.project,
            "concat",
            message=f"mode={args.mode}, clips={len(clip_infos)}",
            artifact=str(output_path),
        )

    with timer_ctx:
        if args.mode == "draft":
            if any(i.is_image for i in clip_infos):
                print(" Stills detected — using normalize path for image segments.", flush=True)
                concat_normalize(
                    clip_infos, output_path, cache_dir, args.preset,
                    force=args.force, reencode_all=False,
                )
            else:
                concat_draft(clips, output_path, args.preset)
        else:
            concat_normalize(
                clip_infos, output_path, cache_dir, args.preset,
                force=args.force,
                reencode_all=(args.mode == "full"),
            )

        print_summary(output_path, clip_infos)
        print(" Done.", flush=True)


if __name__ == "__main__":
    main()
