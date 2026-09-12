#!/usr/bin/env python3
"""Build segment pool and montage manifest from a project clip-map.json."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent
PROJECTS_ROOT = WORKSPACE_ROOT / "projects"

ALL_VIDEO_CLIPS = list(range(1, 12))


def load_clip_map(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve_source_dir(clip_map: dict, project_id: str = "hikmat") -> Path:
    from project_paths import load_project_paths

    paths = load_project_paths(project_id)
    if paths.input_dir.exists():
        for pattern in ("*.mp4", "*.jpg", "*.jpeg", "*.png"):
            if any(paths.input_dir.glob(pattern)):
                return paths.input_dir

    raw = clip_map.get("source_dir", "input")
    return paths.resolve(raw)


def resolve_still_path(clip_map: dict, still: dict) -> Path:
    return resolve_source_dir(clip_map) / still["file"]


def segment_label(clip_index: int, offset: float) -> str:
    if clip_index == 11 and offset >= 0.8:
        return "result-hook"
    if clip_index <= 3 and offset <= 0.15:
        return "materials"
    if clip_index == 11 and offset >= 0.5:
        return "result-close"
    return "process"


def build_pool(clip_map: dict, segment_len: float = 5.0) -> list[dict]:
    total = clip_map["total_duration_sec"]
    pool: list[dict] = []

    for clip in clip_map["clips"]:
        idx = clip["index"]
        for n, offset in enumerate(clip["candidate_offsets"][: clip["max_segments"]]):
            start = clip["master_start"] + clip["duration"] * offset
            end = min(start + segment_len, clip["master_end"], total)
            if end - start < 2.5:
                continue
            pool.append(
                {
                    "id": f"c{idx:02d}_s{n + 1}",
                    "clip_index": idx,
                    "file": clip["file"],
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "duration": round(end - start, 2),
                    "label": segment_label(idx, offset),
                    "offset": offset,
                }
            )
    return pool


def trim_segment(seg: dict, segment_len: float) -> dict:
    duration = seg["end"] - seg["start"]
    if duration <= segment_len:
        return seg
    end = seg["start"] + segment_len
    return {**seg, "end": round(end, 2), "duration": round(segment_len, 2)}


def pick_build_segment(pool: list[dict], clip_index: int, segment_len: float) -> dict:
    """One process slice per clip. Clip 11 ends on final action (0.5), not result (0.85)."""
    clip_segs = [s for s in pool if s["clip_index"] == clip_index]
    if not clip_segs:
        raise ValueError(f"No pool segment for clip {clip_index}")

    if clip_index == 11:
        preferred_offsets = [0.5, 0.1, 0.85]
    else:
        preferred_offsets = [0.5, 0.1, 0.85, 0.3, 0.7, 0.4]

    for off in preferred_offsets:
        for seg in clip_segs:
            if abs(seg["offset"] - off) < 0.05:
                return trim_segment(seg, segment_len)
    return trim_segment(clip_segs[0], segment_len)


def still_segment(clip_map: dict, still: dict, duration: float, label: str) -> dict:
    path = resolve_still_path(clip_map, still)
    return {
        "type": "image",
        "path": str(path),
        "duration": duration,
        "label": label,
        "file": still["file"],
    }


def result_stills(clip_map: dict) -> tuple[dict, dict]:
    stills = clip_map.get("stills") or []
    if not stills:
        raise ValueError("clip-map.json needs stills[] for reveal/return")
    ordered = sorted(stills, key=lambda s: s.get("sort_key", s["file"]))
    reveal = ordered[-1]
    return_still = ordered[-2] if len(ordered) > 1 else ordered[-1]
    return reveal, return_still


SHORT_FORM_STYLE = "reveal-build"


def style_fields() -> dict:
    return {
        "short_form_style": SHORT_FORM_STYLE,
        "hook_type": "result-first",
        "cut_mode": "supercut",
    }


def compose_full_montage(
    clip_map: dict,
    pool: list[dict],
    short_id: str,
    title: str,
    platform: str,
    target: str,
    segment_len: float,
    min_len: int,
    max_len: int,
) -> dict:
    """
    Reveal-Build with full clip coverage:
      REVEAL  — best result still
      BUILD   — one segment per video clip (1→11), ascending
      RETURN  — second result still (or same if only one)
    """
    reveal_still, return_still = result_stills(clip_map)
    reveal = still_segment(clip_map, reveal_still, segment_len, "reveal")
    body = [
        {
            "start": seg["start"],
            "end": seg["end"],
            "label": "build",
            "clip_index": seg["clip_index"],
        }
        for seg in (
            pick_build_segment(pool, idx, segment_len) for idx in ALL_VIDEO_CLIPS
        )
    ]
    close = still_segment(clip_map, return_still, segment_len, "return")
    segments = [reveal, *body, close]
    total = segment_len * len(segments)

    return {
        "id": short_id,
        "title": title,
        **style_fields(),
        "platform": platform,
        "output_kind": "montage",
        "output_name": "reveal-build.mp4",
        "content_type": "carpentry-timelapse",
        "flywheel_stage": "n/a",
        "parent_chapter": "n/a",
        "aspect": "9:16",
        "target": target,
        "min_len": min_len,
        "max_len": max_len,
        "segment_len_sec": segment_len,
        "duration_est": round(total, 1),
        "segments": segments,
        "rendered": False,
    }


def build_manifest(clip_map: dict, pool: list[dict]) -> dict:
    # One reveal-build montage per platform — same segments, different segment_len only.
    montage_specs = [
        ("yt_full", "Reveal-Build", "youtube", "yt-shorts", 5.0, 30, 90),
        ("tiktok_full", "Reveal-Build", "tiktok", "tiktok", 3.5, 15, 90),
        ("reels_full", "Reveal-Build", "reels", "instagram", 5.0, 30, 90),
    ]

    shorts = [
        compose_full_montage(clip_map, pool, *spec) for spec in montage_specs
    ]

    return {
        "version": "1.2",
        "source": clip_map["source"],
        "stem": "hikmat",
        "series_id": "hikmat",
        "planned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "planner_model": "compose_shorts.py",
        "content_type": "carpentry-timelapse",
        "short_form_style": SHORT_FORM_STYLE,
        "output_layout": {
            "montage": "deliverables/{platform}/reveal-build.mp4",
        },
        "review": {
            "status": "draft",
            "notes": "Platform-separated deliverables under output/hikmat/deliverables/.",
        },
        "chapters": [],
        "shorts": shorts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build hikmat segment pool + montage manifest")
    parser.add_argument(
        "--clip-map",
        default=str(PROJECTS_ROOT / "hikmat" / "clip-map.json"),
        help="Path to clip-map.json",
    )
    parser.add_argument(
        "--output-dir",
        help="Plan output directory (default: output/{project}/plan from clip-map stem)",
    )
    parser.add_argument("--project", default="hikmat", help="Project ID for default paths")
    args = parser.parse_args()

    clip_map = load_clip_map(Path(args.clip_map))
    pool = build_pool(clip_map)
    manifest = build_manifest(clip_map, pool)

    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        from project_paths import load_project_paths

        paths = load_project_paths(args.project)
        paths.ensure_dirs()
        out_dir = paths.plan_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    pool_path = out_dir / "segment-pool.json"
    manifest_path = out_dir / "manifest.json"

    pool_path.write_text(
        json.dumps(
            {
                "source": clip_map["source"],
                "segment_len_default": 5.0,
                "segment_count": len(pool),
                "segments": pool,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f" Segment pool: {pool_path} ({len(pool)} candidates)")
    print(f" Manifest: {manifest_path} ({len(manifest['shorts'])} shorts)")
    for short in manifest["shorts"]:
        dur = short.get("duration_est", "?")
        segs = len(short.get("segments") or [])
        kind = "montage" if short.get("segments") else "single"
        print(f"   {short['id']}  {dur}s  [{kind} x{segs}]  {short['title']}")


if __name__ == "__main__":
    main()
