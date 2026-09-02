#!/usr/bin/env python3
"""
Transcribe local video — planning is done by Cursor agent, not a local LLM.

Modes:
  transcribe (default) — extract audio + Whisper segments + optional Vosk words
  render               — ffmpeg cut from manifest or inline --start/--end
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from transcribe import (
    AUDIO_DIR,
    SUB_DIR,
    extract_audio,
    run_cmd,
    transcribe_vosk_words,
    transcribe_whisper,
)

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

for d in [INPUT_DIR, AUDIO_DIR, SUB_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def cut_video(input_video: Path, start: float, end: float, aspect: str, output_path: Path) -> None:
    duration = end - start
    print(f" Rendering clip: {output_path.name} ({start}s → {end}s)")

    vf = "scale=1920:1080"
    if aspect == "9:16":
        vf = "crop=ih*(9/16):ih,scale=1080:1920"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", str(input_video),
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-c:a", "aac",
        str(output_path),
    ]
    run_cmd(cmd)


def render_from_manifest(manifest_path: Path) -> None:
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    source = Path(manifest["source"])
    if not source.is_absolute():
        source = BASE_DIR.parent / source
    if not source.exists():
        print(f" Source not found: {source}")
        sys.exit(1)

    stem = manifest["stem"]
    out_dir = OUTPUT_DIR / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    chapters_dir = out_dir / "chapters"
    shorts_dir = out_dir / "shorts"
    chapters_dir.mkdir(exist_ok=True)
    shorts_dir.mkdir(exist_ok=True)

    for chapter in manifest.get("chapters") or []:
        out_file = chapters_dir / f"{chapter['id']}_{chapter['title'][:40].replace(' ', '_')}.mp4"
        cut_video(source, chapter["start"], chapter["end"], chapter.get("aspect", "16:9"), out_file)

    for short in manifest.get("shorts") or []:
        out_file = shorts_dir / f"{short['id']}_{short['title'][:40].replace(' ', '_')}.mp4"
        cut_video(source, short["start"], short["end"], short.get("aspect", "9:16"), out_file)

    print(f" Render complete → {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="Content pipeline — transcribe or render")
    parser.add_argument("--mode", choices=["transcribe", "render"], default="transcribe")
    parser.add_argument("--input", help="Video filename inside input/ (transcribe mode)")
    parser.add_argument("--manifest", help="Path to manifest.json (render mode)")
    parser.add_argument("--start", type=float, help="Manual cut start (render fallback)")
    parser.add_argument("--end", type=float, help="Manual cut end (render fallback)")
    parser.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    parser.add_argument("--output-name", default="clip.mp4", help="Output filename for manual render")
    parser.add_argument("--vosk", action="store_true", help="Also run Vosk word-level transcript")
    parser.add_argument("--vosk-model", help="Path to Vosk model directory")
    args = parser.parse_args()

    if args.mode == "render":
        if args.manifest:
            render_from_manifest(Path(args.manifest))
            return
        if not args.input or args.start is None or args.end is None:
            print(" Render mode requires --manifest OR (--input + --start + --end)")
            sys.exit(1)
        video_path = INPUT_DIR / args.input
        if not video_path.exists():
            print(f" File not found: {video_path}")
            sys.exit(1)
        cut_video(video_path, args.start, args.end, args.aspect, OUTPUT_DIR / args.output_name)
        return

    if not args.input:
        print(" Transcribe mode requires --input")
        sys.exit(1)

    video_path = INPUT_DIR / args.input
    if not video_path.exists():
        print(f" File not found: {video_path}")
        sys.exit(1)

    base_name = video_path.stem
    audio_path = AUDIO_DIR / f"{base_name}.wav"
    segments_path = SUB_DIR / f"{base_name}.json"
    words_path = SUB_DIR / f"{base_name}.words.json"

    extract_audio(video_path, audio_path)
    transcribe_whisper(audio_path, segments_path)

    if args.vosk:
        transcribe_vosk_words(audio_path, words_path, model_path=args.vosk_model)

    print(" Transcription complete. Planning cuts → use Cursor agent + manifest.json")


if __name__ == "__main__":
    main()
