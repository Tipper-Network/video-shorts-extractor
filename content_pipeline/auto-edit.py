#!/usr/bin/env python3
"""Apply editing skills: SFX allocation + dynamic zoom via MoviePy."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    VideoFileClip,
    vfx,
)

from sfx_resolver import load_triggers, resolve_sfx

ZOOM_INTERVAL = 4.0
ZOOM_FACTOR = 1.15
SFX_VOLUME = 0.4
SFX_COOLDOWN = 0.8


def apply_word_sfx(video_clip, transcript_words: list[dict]):
    """Overlay SFX at trigger words using on-demand resolver."""
    triggers = load_triggers()
    audio_tracks = [video_clip.audio]
    last_sfx_time = -1.0

    for item in transcript_words:
        clean_word = item["word"].lower().strip(".,!?")
        start_time = item["start"]

        if clean_word not in triggers:
            continue
        if (start_time - last_sfx_time) <= SFX_COOLDOWN:
            continue

        sfx_path = resolve_sfx(clean_word)
        if not sfx_path or not sfx_path.exists():
            continue

        sfx_clip = AudioFileClip(str(sfx_path)).set_start(start_time).volumex(SFX_VOLUME)
        audio_tracks.append(sfx_clip)
        last_sfx_time = start_time

    if len(audio_tracks) == 1:
        return video_clip

    final_audio = CompositeAudioClip(audio_tracks)
    return video_clip.set_audio(final_audio)


def apply_dynamic_zooms(video_clip, interval=ZOOM_INTERVAL, factor=ZOOM_FACTOR):
    duration = video_clip.duration
    subclips = []
    current_time = 0.0
    is_zoomed = False

    while current_time < duration:
        end_time = min(current_time + interval, duration)
        segment = video_clip.subclip(current_time, end_time)

        if is_zoomed:
            zoomed_segment = segment.fx(vfx.resize, factor)
            w, h = zoomed_segment.size
            orig_w, orig_h = video_clip.size
            x1 = (w - orig_w) / 2
            y1 = (h - orig_h) / 2
            segment = zoomed_segment.crop(x1=x1, y1=y1, width=orig_w, height=orig_h)

        subclips.append(segment)
        is_zoomed = not is_zoomed
        current_time = end_time

    return CompositeVideoClip(subclips)


def process_video(
    input_path: str | Path,
    output_path: str | Path,
    words_json_path: str | Path | None = None,
    zoom: bool = True,
    sfx: bool = True,
) -> None:
    video = VideoFileClip(str(input_path))

    if sfx and words_json_path and os.path.exists(words_json_path):
        with open(words_json_path, encoding="utf-8") as f:
            transcript_data = json.load(f)
        video = apply_word_sfx(video, transcript_data)

    if zoom:
        video = apply_dynamic_zooms(video)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    video.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Apply SFX + dynamic zoom to a video")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--words", help="Vosk word-level JSON for SFX triggers")
    parser.add_argument("--no-zoom", action="store_true")
    parser.add_argument("--no-sfx", action="store_true")
    args = parser.parse_args()

    process_video(
        args.input,
        args.output,
        words_json_path=args.words,
        zoom=not args.no_zoom,
        sfx=not args.no_sfx,
    )


if __name__ == "__main__":
    main()
