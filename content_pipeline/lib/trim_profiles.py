"""Silence/filler trim presets — mapped from platform skills."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

_PIPELINE = Path(__file__).resolve().parents[1]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

TrimLevel = Literal["off", "light", "moderate", "aggressive"]


@dataclass(frozen=True)
class TrimProfile:
    """Silence-trim preset: ffmpeg long-pause or auto-editor margin."""

    level: TrimLevel
    method: str  # ffmpeg | auto-editor
    min_silence: float | None = None
    threshold_db: float | None = None
    margin: str | None = None
    description: str = ""


PROFILES: dict[TrimLevel, TrimProfile | None] = {
    "off": None,
    # youtube-chunks: gaps > 2.5s
    "light": TrimProfile(
        level="light",
        method="ffmpeg",
        min_silence=2.5,
        threshold_db=-40.0,
        description="Chunks. Drop gaps longer than 2.5s. Leave 0.2s so the next word is not clipped.",
    ),
    "moderate": TrimProfile(
        level="moderate",
        method="auto-editor",
        margin="0.6sec",
        description="Shorts. 0.6s margin drops a breath between clauses and keeps the breath before the next word, including the land.",
    ),
    # tiktok-shorts: gaps > 0.4s, aggressive
    "aggressive": TrimProfile(
        level="aggressive",
        method="auto-editor",
        margin="0.4sec",
        description="TikTok — tight pacing, filler reduction via tight margins",
    ),
}

def resolve_trim_level(
    *,
    deliverable: str,
    clip_override: str | None = None,
    manifest_default: str | None = None,
    project_default: str | None = None,
) -> TrimLevel:
    """Pick how hard to trim silence on a clip.

    Precedence: clip override → manifest default → project default → deliverable.
    A short defaults to ``moderate``. A chapter defaults to ``light``.
    Platform names do not choose a trim.

    Args:
        deliverable: ``short`` or ``chapter``.
        clip_override: Per-clip ``trim`` value if the planner set one.
        manifest_default: Manifest-wide default trim.
        project_default: ``pipeline.json`` project default.

    Returns:
        One of ``off``, ``light``, ``moderate``, ``aggressive``.
    """
    for value in (clip_override, manifest_default, project_default):
        if value and value in PROFILES:
            return value  # type: ignore[return-value]
    if deliverable == "short":
        return "moderate"
    if deliverable == "chapter":
        return "light"
    return "off"


def get_profile(level: TrimLevel) -> TrimProfile | None:
    """Look up the ffmpeg / auto-editor settings for a trim level.

    Args:
        level: ``off``, ``light``, ``moderate``, or ``aggressive``.

    Returns:
        The preset, or ``None`` when trim is ``off``.
    """
    return PROFILES.get(level)
