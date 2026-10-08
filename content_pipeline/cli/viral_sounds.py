#!/usr/bin/env python3
"""Stage-2 viral sounds — tier-A mute+beep + word-trigger SFX (no zoom)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from moviepy import AudioArrayClip, AudioFileClip, CompositeAudioClip, VideoFileClip, afx
from scipy.io import wavfile

_PIPELINE = Path(__file__).resolve().parents[1]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from sfx_resolver import load_triggers, resolve_sfx  # noqa: E402

CONFIG = _PIPELINE / "config"
CENSOR_PATH = CONFIG / "censor_words.json"
SFX_VOLUME = 0.4
BEEP_VOLUME = 0.55
SFX_COOLDOWN = 0.8


def load_censor() -> tuple[set[str], dict]:
    data = json.loads(CENSOR_PATH.read_text(encoding="utf-8"))
    words = {w.lower() for w in data.get("words", [])}
    return words, data.get("audio", {})


def clean_token(raw: str) -> str:
    return re.sub(r"^[^\w']+|[^\w']+$", "", raw, flags=re.UNICODE).lower()


def make_beep(duration: float, freq: float = 1000.0, sr: int = 44100) -> AudioArrayClip:
    n = max(1, int(duration * sr))
    t = np.linspace(0, duration, n, endpoint=False)
    wave = 0.35 * np.sin(2 * np.pi * freq * t)
    # short fade to avoid clicks
    fade = min(n // 10, int(0.01 * sr))
    if fade > 0:
        wave[:fade] *= np.linspace(0, 1, fade)
        wave[-fade:] *= np.linspace(1, 0, fade)
    arr = np.column_stack([wave, wave]).astype(np.float32)
    return AudioArrayClip(arr, fps=sr)


def apply_sounds(
    video_path: Path,
    words: list[dict],
    output: Path,
) -> None:
    censor, audio_cfg = load_censor()
    pad_before = float(audio_cfg.get("pad_ms_before", 40)) / 1000.0
    pad_after = float(audio_cfg.get("pad_ms_after", 80)) / 1000.0
    triggers = load_triggers()

    clip = VideoFileClip(str(video_path))
    if clip.audio is None:
        raise SystemExit("Input has no audio track")

    audio = clip.audio
    extras: list = []
    last_sfx = -1.0
    mute_windows: list[tuple[float, float]] = []
    beep_count = 0
    sfx_count = 0

    for item in words:
        token = clean_token(item["word"])
        if not token:
            continue
        start = float(item["start"])
        end = float(item["end"])
        if end <= start:
            end = start + 0.12

        if token in censor:
            m0 = max(0.0, start - pad_before)
            m1 = min(float(clip.duration), end + pad_after)
            mute_windows.append((m0, m1))
            beep = make_beep(max(0.08, m1 - m0)).with_start(m0).with_volume_scaled(BEEP_VOLUME)
            extras.append(beep)
            beep_count += 1
            continue

        if token not in triggers:
            continue
        if (start - last_sfx) <= SFX_COOLDOWN:
            continue
        path = resolve_sfx(token)
        if not path or not Path(path).exists():
            continue
        sfx = AudioFileClip(str(path)).with_start(start).with_volume_scaled(SFX_VOLUME)
        # trim long SFX
        if sfx.duration > 1.2:
            sfx = sfx.subclipped(0, 1.2)
        extras.append(sfx)
        last_sfx = start
        sfx_count += 1

    for m0, m1 in mute_windows:
        audio = audio.with_effects([afx.MultiplyVolume(0.0, start_time=m0, end_time=m1)])

    mixed = CompositeAudioClip([audio, *extras]) if extras else audio
    out = clip.with_audio(mixed)
    output.parent.mkdir(parents=True, exist_ok=True)
    print(f" Sounds: {beep_count} beeps, {sfx_count} triggers → {output}")
    out.write_videofile(
        str(output),
        codec="libx264",
        audio_codec="aac",
        fps=clip.fps or 30,
        preset="fast",
        threads=4,
        logger="bar",
    )
    clip.close()
    out.close()


def main() -> None:
    p = argparse.ArgumentParser(description="Stage-2 mute+beep + trigger SFX")
    p.add_argument("--input", required=True, type=Path, help="Usually stage1 captioned mp4")
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--words", required=True, type=Path, help="words.json from stage1")
    args = p.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Missing input: {args.input}")
    if not args.words.exists():
        raise SystemExit(f"Missing words: {args.words}")

    words = json.loads(args.words.read_text(encoding="utf-8"))
    apply_sounds(args.input, words, args.output)


if __name__ == "__main__":
    main()
