"""Silence/filler trim presets — mapped from platform skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TrimLevel = Literal["off", "light", "moderate", "aggressive"]


@dataclass(frozen=True)
class TrimProfile:
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
}


def resolve_trim_level(
    *,
    clip_target: str | None = None,
    clip_override: str | None = None,
    manifest_default: str | None = None,
    project_default: str | None = None,
) -> TrimLevel:
    for value in (clip_override, manifest_default, TARGET_DEFAULTS.get(clip_target or "", ""), project_default):
        if value and value in PROFILES:
            return value  # type: ignore[return-value]
    return "off"


def get_profile(level: TrimLevel) -> TrimProfile | None:
    return PROFILES.get(level)
