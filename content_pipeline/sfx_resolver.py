#!/usr/bin/env python3
"""On-demand SFX resolution — API fetch with ephemeral cache, synthetic fallback."""

from __future__ import annotations

import hashlib
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from env_loader import load_env

load_env()

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / ".cache" / "sfx"
TRIGGERS_PATH = BASE_DIR / "sfx_triggers.json"

DEFAULT_TRIGGERS = {
    "important": {"query": "pop notification", "synthetic": "pop"},
    "money": {"query": "cash register coin", "synthetic": "cha_ching"},
    "wrong": {"query": "buzzer wrong answer", "synthetic": "buzzer"},
    "correct": {"query": "ding success", "synthetic": "ding"},
    "stop": {"query": "whoosh transition", "synthetic": "whoosh"},
}


def load_triggers() -> dict:
    """Load ``sfx_triggers.json`` or the built-in word → query map.

    Returns:
        ``{word: {query, synthetic}}`` dict.
    """
    if TRIGGERS_PATH.exists():
        with open(TRIGGERS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_TRIGGERS


def _cache_path(key: str, ext: str = ".mp3") -> Path:
    """Hashed cache path under ``.cache/sfx/``.

    Args:
        key: Cache key (provider + query).
        ext: File suffix including the dot.

    Returns:
        Destination path (file may not exist yet).
    """
    digest = hashlib.sha256(key.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{digest}{ext}"


def _download(url: str, dest: Path) -> bool:
    """Download a URL to ``dest``.

    Args:
        url: HTTP(S) audio URL.
        dest: Local file path.

    Returns:
        True if the file exists and is non-empty.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "content-pipeline/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            dest.write_bytes(resp.read())
        return dest.stat().st_size > 0
    except Exception as exc:
        print(f"  SFX download failed: {exc}")
        if dest.exists():
            dest.unlink(missing_ok=True)
        return False


def _fetch_freesound(query: str, cache_key: str) -> Path | None:
    """Search Freesound and cache the first preview.

    Args:
        query: Search string.
        cache_key: Local cache identity.

    Returns:
        Cached mp3 path, or ``None`` if no key / no hit.
    """
    token = os.environ.get("FREESOUND_API_KEY")
    if not token:
        return None

    params = urllib.parse.urlencode(
        {"query": query, "token": token, "fields": "id,previews", "page_size": 1}
    )
    url = f"https://freesound.org/apiv2/search/text/?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "content-pipeline/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception as exc:
        print(f"  Freesound search failed: {exc}")
        return None

    results = data.get("results") or []
    if not results:
        return None

    previews = results[0].get("previews") or {}
    preview_url = previews.get("preview-hq-mp3") or previews.get("preview-lq-mp3")
    if not preview_url:
        return None

    dest = _cache_path(f"freesound:{cache_key}", ".mp3")
    if dest.exists() or _download(preview_url, dest):
        return dest
    return None


def _fetch_pixabay(query: str, cache_key: str) -> Path | None:
    """Search Pixabay audio and cache the first hit.

    Args:
        query: Search string.
        cache_key: Local cache identity.

    Returns:
        Cached mp3 path, or ``None`` if no key / no hit.
    """
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        return None

    params = urllib.parse.urlencode({"key": key, "q": query, "per_page": 3})
    url = f"https://pixabay.com/api/audio/?{params}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "content-pipeline/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception as exc:
        print(f"  Pixabay search failed: {exc}")
        return None

    hits = data.get("hits") or []
    if not hits:
        return None

    audio_url = hits[0].get("audio") or hits[0].get("previewURL")
    if not audio_url:
        return None

    dest = _cache_path(f"pixabay:{cache_key}", ".mp3")
    if dest.exists() or _download(audio_url, dest):
        return dest
    return None


def _synthesize(kind: str) -> Path:
    """Generate a short WAV when no API key or network result is available.

    Args:
        kind: ``pop``, ``ding``, ``buzzer``, ``cha_ching``, ``whoosh``, or a 440Hz fallback.

    Returns:
        Cached ``.wav`` path.
    """
    sr = 44100
    dest = _cache_path(f"synthetic:{kind}", ".wav")
    if dest.exists():
        return dest

    duration = 0.35
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    if kind == "pop":
        envelope = np.exp(-t * 40)
        wave = np.random.uniform(-1, 1, len(t)) * envelope * 0.4
    elif kind == "ding":
        wave = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 6)
    elif kind == "buzzer":
        wave = np.sign(np.sin(2 * np.pi * 180 * t)) * np.exp(-t * 3) * 0.35
    elif kind == "cha_ching":
        tone_a = np.sin(2 * np.pi * 1200 * t[: len(t) // 2])
        tone_b = np.sin(2 * np.pi * 1800 * t[len(t) // 2 :])
        wave = np.concatenate([tone_a, tone_b]) * np.exp(-t * 4)
    elif kind == "whoosh":
        noise = np.random.uniform(-1, 1, len(t))
        sweep = np.linspace(0.1, 1.0, len(t))
        wave = noise * sweep * np.exp(-t * 2) * 0.5
    else:
        wave = np.sin(2 * np.pi * 440 * t) * np.exp(-t * 8)

    wave = np.clip(wave, -1.0, 1.0)
    wavfile.write(dest, sr, (wave * 32767).astype(np.int16))
    return dest


def resolve_sfx(trigger_word: str) -> Path | None:
    """Resolve a trigger word to a local audio file.

    Order: cache hit → Freesound → Pixabay → synthetic fallback.

    Args:
        trigger_word: Transcript token (punctuation stripped).

    Returns:
        Local audio path, or ``None`` if the word is not in the trigger map.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    triggers = load_triggers()
    word = trigger_word.lower().strip(".,!?")
    config = triggers.get(word)
    if not config:
        return None

    query = config.get("query", word)
    synthetic = config.get("synthetic", "ding")

    for fetcher, prefix in ((_fetch_freesound, "fs"), (_fetch_pixabay, "px")):
        path = fetcher(query, f"{prefix}:{word}:{query}")
        if path:
            print(f"  SFX [{word}] ← {fetcher.__name__}")
            return path

    path = _synthesize(synthetic)
    print(f"  SFX [{word}] ← synthetic ({synthetic})")
    return path
