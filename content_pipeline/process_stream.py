#!/usr/bin/env python3
"""
Transcribe local video — planning is done by Cursor agent, not a local LLM.

Modes:
  transcribe (default) — YouTube .srt next to the video if present, else Whisper.
                         Optional Vosk words. --whisper forces full-file Whisper.
  render               — ffmpeg cut from manifest or inline --start/--end
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from project_paths import load_project_paths
from transcribe import (
    AUDIO_DIR,
    SUB_DIR,
    extract_audio,
    run_cmd,
    safe_stem,
    transcribe_vosk_words,
    transcribe_whisper,
)

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

for d in [INPUT_DIR, AUDIO_DIR, SUB_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def find_input_video(project_id: str | None, input_name: str | None) -> tuple[Path, str]:
    """Locate the source video in project ``input/`` or legacy ``input/``.

    Args:
        project_id: Project slug, or ``None`` for the pipeline-local ``input/``.
        input_name: Filename inside ``input/``. Required when that folder has more than one video.

    Returns:
        ``(video_path, stem)``. Exits the process if the file is missing or ambiguous.
    """
    if project_id:
        paths = load_project_paths(project_id)
        paths.ensure_dirs()
        if input_name:
            video = paths.input_dir / input_name
            if not video.exists():
                print(f" File not found: {video}")
                sys.exit(1)
            return video, video.stem

        candidates = sorted(
            p
            for p in paths.input_dir.iterdir()
            if p.suffix.lower() in {".mp4", ".mkv", ".mov", ".webm"}
        )
        if len(candidates) == 1:
            return candidates[0], candidates[0].stem
        if len(candidates) > 1:
            print(" Multiple videos in input/ — pass --input filename:")
            for c in candidates:
                print(f"   {c.name}")
            sys.exit(1)
        print(f" No video in {paths.input_dir}")
        sys.exit(1)

    if not input_name:
        print(" Transcribe mode requires --input (or --project with one video in input/)")
        sys.exit(1)
    video_path = INPUT_DIR / input_name
    if not video_path.exists():
        print(f" File not found: {video_path}")
        sys.exit(1)
    return video_path, video_path.stem


def cut_video(input_video: Path, start: float, end: float, aspect: str, output_path: Path) -> None:
    """Cut one window with ffmpeg (legacy render path; prefer ``cut_utils.cut_video``).

    Args:
        input_video: Source mp4.
        start: In-point seconds.
        end: Out-point seconds.
        aspect: ``16:9`` or ``9:16``.
        output_path: Destination mp4.
    """
    duration = end - start
    print(f" Rendering clip: {output_path.name} ({start}s → {end}s)")

    from cut_utils import aspect_filter

    vf = aspect_filter(aspect)

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
    """Legacy batch render: chapters → ``chunks/``, shorts → ``shorts/`` under ``output/{stem}/``.

    Args:
        manifest_path: ``manifest.json`` with ``source``, ``stem``, ``chapters``, ``shorts``.
    """
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    source = Path(manifest["source"])
    if not source.is_absolute():
        source = WORKSPACE_ROOT / source
    if not source.exists():
        print(f" Source not found: {source}")
        sys.exit(1)

    stem = manifest["stem"]
    out_dir = OUTPUT_DIR / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir = out_dir / "chunks"
    shorts_dir = out_dir / "shorts"
    chunks_dir.mkdir(exist_ok=True)
    shorts_dir.mkdir(exist_ok=True)

    for chapter in manifest.get("chapters") or []:
        out_file = chunks_dir / f"{chapter['id']}_{chapter['title'][:40].replace(' ', '_')}.mp4"
        cut_video(source, chapter["start"], chapter["end"], chapter.get("aspect", "16:9"), out_file)

    for short in manifest.get("shorts") or []:
        out_file = shorts_dir / f"{short['id']}_{short['title'][:40].replace(' ', '_')}.mp4"
        cut_video(source, short["start"], short["end"], short.get("aspect", "9:16"), out_file)

    print(f" Render complete → {out_dir}")


def main():
    """CLI: transcribe (YouTube SRT or Whisper) or render a cut from a manifest / clocks."""
    parser = argparse.ArgumentParser(description="Content pipeline — transcribe or render")
    parser.add_argument("--mode", choices=["transcribe", "render"], default="transcribe")
    parser.add_argument("--project", help="Project ID — reads/writes under projects/{id}/")
    parser.add_argument(
        "--input",
        help="One video filename inside project input/ (or legacy input/). "
        "Required when the project has more than one video. "
        "Writes output/transcript/{slug}/ so files do not overwrite.",
    )
    parser.add_argument("--manifest", help="Path to manifest.json (render mode)")
    parser.add_argument("--start", type=float, help="Manual cut start (render fallback)")
    parser.add_argument("--end", type=float, help="Manual cut end (render fallback)")
    parser.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    parser.add_argument("--output-name", default="clip.mp4", help="Output filename for manual render")
    parser.add_argument("--vosk", action="store_true", help="Also run Vosk word-level transcript")
    parser.add_argument("--vosk-model", help="Path to Vosk model directory")
    parser.add_argument("--model", default="small", help="Whisper model size (default: small)")
    parser.add_argument(
        "--whisper",
        action="store_true",
        help="Force full-file Whisper even when a YouTube .srt sits next to the video",
    )
    args = parser.parse_args()

    if args.mode == "render":
        if args.manifest:
            render_from_manifest(Path(args.manifest))
            return
        if not args.input or args.start is None or args.end is None:
            print(" Render mode requires --manifest OR (--input + --start + --end)")
            sys.exit(1)
        video_path, _ = find_input_video(args.project, args.input)
        out = OUTPUT_DIR / args.output_name
        if args.project:
            paths = load_project_paths(args.project)
            out = paths.deliverables_dir / "chunks" / args.output_name
            out.parent.mkdir(parents=True, exist_ok=True)
        cut_video(video_path, args.start, args.end, args.aspect, out)
        return

    video_path, base_name = find_input_video(args.project, args.input)
    slug = safe_stem(video_path.name)

    from contextlib import nullcontext

    if args.project:
        from pipeline_log import StageTimer

        paths = load_project_paths(args.project)
        paths.ensure_dirs()
        # Multi-file jobs pass --input; keep a per-video folder so the next
        # transcribe does not clobber the per-video clock file. Single auto-detected
        # video still writes the legacy output/transcript/transcript.txt.
        if args.input:
            audio_path = paths.audio_cache_dir / f"{slug}.wav"
            out_dir = paths.transcript_dir / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            segments_path = out_dir / "segments.json"
            words_path = out_dir / "words.json"
            from srt_to_text import clock_txt_path

            transcript_txt = clock_txt_path(out_dir)
        else:
            audio_path = paths.audio_cache_dir / f"{base_name}.wav"
            segments_path = paths.segments_json_path()
            words_path = paths.words_json_path()
            transcript_txt = paths.transcript_txt_path()
        timer_ctx = StageTimer(args.project, "transcribe", message=video_path.name)
    else:
        paths = None
        audio_path = AUDIO_DIR / f"{slug}.wav"
        segments_path = SUB_DIR / f"{slug}.json"
        words_path = SUB_DIR / f"{slug}.words.json"
        transcript_txt = SUB_DIR / f"{slug}.txt"
        timer_ctx = nullcontext()

    from srt_to_text import find_sidecar_srt, write_clocks_from_srt

    srt_path = None if args.whisper else find_sidecar_srt(video_path)

    with timer_ctx:
        if srt_path:
            print(f" Using YouTube SRT {srt_path.name} — skip full-file Whisper")
            write_clocks_from_srt(
                srt_path,
                segments_json_path=segments_path,
                transcript_txt_path=transcript_txt,
            )
            if args.vosk:
                extract_audio(video_path, audio_path)
                transcribe_vosk_words(audio_path, words_path, model_path=args.vosk_model)
        else:
            extract_audio(video_path, audio_path)
            transcribe_whisper(
                audio_path,
                segments_path,
                model_size=args.model,
                transcript_txt_path=transcript_txt,
            )
            if args.vosk:
                transcribe_vosk_words(audio_path, words_path, model_path=args.vosk_model)

    print(f" Transcript: {transcript_txt}")
    print(" Planning cuts → use Cursor agent + manifest.json")


if __name__ == "__main__":
    main()
