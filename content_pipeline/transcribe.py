#!/usr/bin/env python3
"""Shared transcription utilities — Whisper segments + optional Vosk word timestamps."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from faster_whisper import WhisperModel

from env_loader import load_env

load_env()

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
SUB_DIR = BASE_DIR / "subtitles"


def run_cmd(cmd: list[str]) -> str:
    print(f" Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f" Error: {result.stderr}")
        sys.exit(1)
    return result.stdout


def extract_audio(video_path: Path, audio_path: Path) -> None:
    """Extract 16kHz mono audio optimized for speech recognition."""
    print(" Extracting audio from video...")
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(audio_path),
    ]
    run_cmd(cmd)


def transcribe_whisper(
    audio_path: Path,
    transcript_json_path: Path,
    model_size: str = "small",
) -> list[dict]:
    """Full segment transcript via Faster-Whisper."""
    print(" Running Faster-Whisper transcription...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(audio_path), beam_size=5)

    segments_data = [
        {"start": round(seg.start, 2), "end": round(seg.end, 2), "text": seg.text.strip()}
        for seg in segments
    ]

    transcript_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(transcript_json_path, "w", encoding="utf-8") as f:
        json.dump(segments_data, f, indent=2, ensure_ascii=False)

    print(f" Saved {len(segments_data)} segments → {transcript_json_path}")
    return segments_data


def transcribe_vosk_words(
    audio_path: Path,
    words_json_path: Path,
    model_path: str | None = None,
) -> list[dict]:
    """
    Word-level timestamps via Vosk (for SFX allocation).
    Requires: pip install vosk + a Vosk model (VOSK_MODEL_PATH env or --vosk-model).
    """
    import os
    import wave

    import vosk

    model_path = model_path or os.environ.get("VOSK_MODEL_PATH")
    if not model_path or not Path(model_path).exists():
        print(" Vosk model not found — set VOSK_MODEL_PATH or pass model_path.")
        print(" Skipping word-level transcript.")
        return []

    print(f" Running Vosk word-level transcription ({model_path})...")
    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    words: list[dict] = []
    with wave.open(str(audio_path), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            print(" Vosk requires 16kHz mono PCM WAV — re-extract audio first.")
            return []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                words.extend(result.get("result") or [])

        final = json.loads(rec.FinalResult())
        words.extend(final.get("result") or [])

    word_data = [
        {"word": w["word"], "start": round(w["start"], 2), "end": round(w["end"], 2)}
        for w in words
    ]

    words_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(words_json_path, "w", encoding="utf-8") as f:
        json.dump(word_data, f, indent=2, ensure_ascii=False)

    print(f" Saved {len(word_data)} words → {words_json_path}")
    return word_data
