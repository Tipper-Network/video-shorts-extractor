#!/usr/bin/env python3
"""Build segment pool and montage manifest from a project clip-map.json."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"


def load_clip_map(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


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


def pick(pool: list[dict], clip_index: int, label: str | None = None) -> dict | None:
    matches = [s for s in pool if s["clip_index"] == clip_index]
    if label:
        matches = [s for s in matches if s["label"] == label]
    if not matches:
        matches = [s for s in pool if s["clip_index"] == clip_index]
    return matches[0] if matches else None


def hook_segment(pool: list[dict]) -> dict:
    for preferred in ("result-hook", "result-close", "process"):
        seg = pick(pool, 11, preferred)
        if seg:
            return {**seg, "label": "result-hook"}
    raise ValueError("No hook segment found in clip 11")


def close_segment(pool: list[dict], hook: dict) -> dict:
    for seg in pool:
        if seg["clip_index"] == 11 and seg["id"] != hook["id"]:
            return {**seg, "label": "result-close"}
    return {**hook, "label": "result-close"}


def trim_segment(seg: dict, segment_len: float) -> dict:
    duration = seg["end"] - seg["start"]
    if duration <= segment_len:
        return seg
    end = seg["start"] + segment_len
    return {**seg, "end": round(end, 2), "duration": round(segment_len, 2)}


def compose_montage(
    pool: list[dict],
    short_id: str,
    title: str,
    target: str,
    clip_indices: list[int],
    segment_len: float,
    min_len: int,
    max_len: int,
) -> dict:
    hook = trim_segment(hook_segment(pool), segment_len)
    body: list[dict] = []
    for idx in clip_indices:
        seg = pick(pool, idx)
        if seg and seg["id"] not in {hook["id"], *(b["id"] for b in body)}:
            body.append(trim_segment(seg, segment_len))

    body.sort(key=lambda s: s["start"])
    close = trim_segment(close_segment(pool, hook), segment_len)

    segments = [hook, *body, close]
    total = sum(s["end"] - s["start"] for s in segments)

    return {
        "id": short_id,
        "title": title,
        "hook_type": "result-first",
        "content_type": "carpentry-timelapse",
        "flywheel_stage": "n/a",
        "parent_chapter": "n/a",
        "aspect": "9:16",
        "target": target,
        "min_len": min_len,
        "max_len": max_len,
        "segment_len_sec": segment_len,
        "duration_est": round(total, 1),
        "segments": [
            {
                "start": s["start"],
                "end": s["end"],
                "label": s["label"],
                "clip_index": s["clip_index"],
            }
            for s in segments
        ],
        "rendered": False,
    }


def single_clip_short(
    short_id: str,
    title: str,
    target: str,
    clip: dict,
    start_ratio: float,
    end_ratio: float,
    min_len: int,
    max_len: int,
) -> dict:
    start = clip["master_start"] + clip["duration"] * start_ratio
    end = clip["master_start"] + clip["duration"] * end_ratio
    return {
        "id": short_id,
        "title": title,
        "hook_type": "result-first",
        "content_type": "carpentry-timelapse",
        "flywheel_stage": "n/a",
        "parent_chapter": "n/a",
        "aspect": "9:16",
        "target": target,
        "min_len": min_len,
        "max_len": max_len,
        "start": round(start, 2),
        "end": round(end, 2),
        "duration_est": round(end - start, 1),
        "clip_index": clip["index"],
        "rendered": False,
    }


def build_manifest(clip_map: dict, pool: list[dict]) -> dict:
    clips = {c["index"]: c for c in clip_map["clips"]}

    montage_specs = [
        ("sh01", "Full build montage — YouTube", "yt-shorts", [1, 3, 4, 5, 7, 10], 5.0, 30, 60),
        ("sh02", "Early to late build — YouTube", "yt-shorts", [1, 2, 4, 6, 8, 9], 5.0, 30, 60),
        ("sh03", "Mid build focus — YouTube", "yt-shorts", [3, 5, 6, 7, 8, 10], 5.0, 30, 60),
        ("sh04", "Compact journey — YouTube", "yt-shorts", [1, 5, 7, 11], 5.0, 30, 60),
        ("sh05", "Fast timelapse — TikTok", "tiktok", [1, 3, 5, 7, 9, 10], 3.5, 15, 60),
        ("sh06", "Rapid cuts — TikTok", "tiktok", [2, 4, 6, 8, 10], 3.5, 15, 60),
        ("sh07", "Dense build — TikTok", "tiktok", [1, 4, 5, 6, 7, 8, 9], 3.5, 15, 60),
        ("sh08", "Slow reveal — Reels", "instagram", [1, 4, 5, 7, 10], 6.0, 30, 90),
        ("sh09", "Workshop story — Reels", "instagram", [3, 6, 7, 8, 10], 6.0, 30, 90),
    ]

    shorts = [compose_montage(pool, *spec) for spec in montage_specs]

    shorts.append(
        single_clip_short(
            "sh10",
            "Long session — main build clip",
            "instagram",
            clips[5],
            0.15,
            0.55,
            30,
            90,
        )
    )
    shorts.append(
        single_clip_short(
            "sh11",
            "Final session — result build",
            "yt-shorts",
            clips[11],
            0.55,
            0.95,
            30,
            60,
        )
    )

    return {
        "version": "1.0",
        "source": clip_map["source"],
        "stem": "hikmat",
        "series_id": "hikmat",
        "planned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "planner_model": "compose_shorts.py",
        "content_type": "carpentry-timelapse",
        "review": {
            "status": "draft",
            "notes": "Heuristic timestamps — review hooks and dead frames before publish.",
        },
        "chapters": [],
        "shorts": shorts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build hikmat segment pool + montage manifest")
    parser.add_argument(
        "--clip-map",
        default=str(PROJECTS_DIR / "hikmat" / "clip-map.json"),
        help="Path to clip-map.json",
    )
    parser.add_argument(
        "--output-dir",
        default=str(BASE_DIR / "output" / "hikmat"),
        help="Output directory for segment-pool.json and manifest.json",
    )
    args = parser.parse_args()

    clip_map = load_clip_map(Path(args.clip_map))
    pool = build_pool(clip_map)
    manifest = build_manifest(clip_map, pool)

    out_dir = Path(args.output_dir)
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
        kind = "montage" if short.get("segments") else "single"
        print(f"   {short['id']}  {dur}s  [{kind}]  {short['title']}")


if __name__ == "__main__":
    main()
