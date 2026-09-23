"""Silence/filler trim presets — mapped from platform skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

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
        description="YouTube chapters — strip long pauses only",
    ),
    # youtube-shorts: gaps > 0.6s
    "moderate": TrimProfile(
        level="moderate",
        method="auto-editor",
        margin="0.6sec",
        description="YouTube Shorts / Reels — moderate pacing",
    ),
    # tiktok-shorts: gaps > 0.4s, aggressive
    "aggressive": TrimProfile(
        level="aggressive",
        method="auto-editor",
        margin="0.4sec",
        description="TikTok — tight pacing, filler reduction via tight margins",
    ),
}

# Default trim level per platform target when not specified on clip/manifest
TARGET_DEFAULTS: dict[str, TrimLevel] = {
    "youtube": "light",
    "yt-shorts": "moderate",
    "tiktok": "aggressive",
    "instagram": "moderate",
    "reels": "moderate",
}


def resolve_trim_level(
    *,
    clip_target: str | None = None,
    clip_override: str | None = None,
    manifest_default: str | None = None,
    project_default: str | None = None,
) -> TrimLevel:
    """Pick how hard to trim silence on a clip.

    Precedence: clip override → manifest default → platform target → project default → ``off``.

    Args:
        clip_target: Manifest platform key (``youtube``, ``yt-shorts``, ``tiktok``, …).
        clip_override: Per-clip ``trim`` value if the planner set one.
        manifest_default: Manifest-wide default trim.
        project_default: ``pipeline.json`` project default.

    Returns:
        One of ``off``, ``light``, ``moderate``, ``aggressive``.
    """
    for value in (clip_override, manifest_default, TARGET_DEFAULTS.get(clip_target or "", ""), project_default):
        if value and value in PROFILES:
            return value  # type: ignore[return-value]
    return "off"


def get_profile(level: TrimLevel) -> TrimProfile | None:
    """Look up the ffmpeg / auto-editor settings for a trim level.

    Args:
        level: ``off``, ``light``, ``moderate``, or ``aggressive``.

    Returns:
        The preset, or ``None`` when trim is ``off``.
    """
    return PROFILES.get(level)
