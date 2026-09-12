#!/usr/bin/env python3
"""Batch-render chapters and shorts from an approved manifest.json."""

from __future__ import annotations

import argparse
import json
import sys
from contextlib import nullcontext
from pathlib import Path

from cut_utils import render_clip_entry
from project_config import load_pipeline
from project_paths import load_project_paths
from trim_profiles import resolve_trim_level

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent

# Manifest target → deliverables subfolder
PLATFORM_SUBDIRS = {
    "yt-shorts": "youtube",
    "youtube": "youtube",
    "tiktok": "tiktok",
    "instagram": "reels",
}


def short_output_path(deliverables_dir: Path, short: dict) -> Path:
    """Route renders to deliverables/{platform}/."""
    platform = short.get("platform") or PLATFORM_SUBDIRS.get(short.get("target", ""), "other")
    subdir = deliverables_dir / platform
    subdir.mkdir(parents=True, exist_ok=True)
    name = short.get("output_name") or f"{short['id']}.mp4"
    if not name.endswith(".mp4"):
        name = f"{name}.mp4"
    return subdir / name


def chapter_output_path(deliverables_dir: Path, chapter: dict) -> Path:
    """Route chapter renders to deliverables/{platform}/."""
    platform = chapter.get("platform") or PLATFORM_SUBDIRS.get(chapter.get("target", "youtube"), "youtube")
    subdir = deliverables_dir / platform
    subdir.mkdir(parents=True, exist_ok=True)
    if chapter.get("output_name"):
        name = chapter["output_name"]
    else:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in chapter["title"][:40])
        name = f"{chapter['id']}_{safe}.mp4"
    if not name.endswith(".mp4"):
        name = f"{name}.mp4"
    return subdir / name


def resolve_source(manifest: dict, project_id: str | None = None) -> Path:
    source = Path(manifest["source"])
    if source.is_absolute() and source.exists():
        return source

    search_roots: list[Path] = []
    if project_id:
        search_roots.append(load_project_paths(project_id).root)
    search_roots.extend([BASE_DIR, WORKSPACE_ROOT])

    for base in search_roots:
        candidate = base / source
        if candidate.exists():
            return candidate
    # legacy: path already included content_pipeline/ prefix
    for base in search_roots:
        for prefix in ("content_pipeline/", ""):
            candidate = base / prefix / source if prefix else base / source
            if candidate.exists():
                return candidate
    return WORKSPACE_ROOT / source


def render_manifest(
    manifest_path: Path,
    polish: bool = False,
    only: str | None = None,
    project_id: str | None = None,
    skip_trim: bool = False,
) -> Path:
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    source = resolve_source(manifest, project_id)
    if not source.exists():
        print(f" Source not found: {source}")
        sys.exit(1)

    project_id = project_id or manifest.get("series_id") or manifest.get("stem")
    pipeline = load_pipeline(project_id) if project_id else {}
    render_cfg = pipeline.get("modules", {}).get("render", {})
    trim_enabled = render_cfg.get("trim_on_render", True) and not skip_trim

    paths = load_project_paths(project_id) if project_id else None
    if paths:
        paths.ensure_dirs()

    chapter_defaults = pipeline.get("chapters", {})
    short_defaults = pipeline.get("shorts", {})

    stem = manifest["stem"]
    out_dir = paths.root if paths else WORKSPACE_ROOT / "projects" / stem
    plan_dir = paths.plan_dir if paths else out_dir / "output" / "plan"
    deliverables_dir = paths.deliverables_dir if paths else out_dir / "output" / "deliverables"

    manifest_trim_default = manifest.get("render", {}).get("default_trim")
    rendered = []

    work_items: list[tuple[str, dict, str]] = []
    for chapter in manifest.get("chapters") or []:
        if only and chapter["id"] != only:
            continue
        work_items.append(("chapter", chapter, "16:9"))
    for short in manifest.get("shorts") or []:
        if only and short["id"] != only:
            continue
        work_items.append(("short", short, "9:16"))

    progress_ctx = nullcontext()
    if project_id and work_items:
        from pipeline_log import ProgressTracker

        progress_ctx = ProgressTracker(
            project_id,
            "render_shorts",
            len(work_items),
            unit="clip",
            message=f"rendering {len(work_items)} clips",
        )

    item_idx = 0
    with progress_ctx as progress:
        for chapter in manifest.get("chapters") or []:
            if only and chapter["id"] != only:
                continue
            item_idx += 1
            if progress:
                progress.update(item_idx, item=chapter["id"], message=chapter["title"][:50])

            out_file = chapter_output_path(deliverables_dir, chapter)
            rel = out_file.relative_to(WORKSPACE_ROOT)
            print(f" Chapter {chapter['id']}: {chapter['title']} → {rel} [{chapter.get('cut_mode', 'contiguous')}]")

            trim_level = "off"
            if trim_enabled:
                trim_level = resolve_trim_level(
                    clip_target=chapter.get("target", "youtube"),
                    clip_override=chapter.get("trim"),
                    manifest_default=manifest_trim_default,
                    project_default=chapter_defaults.get("default_trim"),
                )

            render_clip_entry(
                source,
                chapter,
                chapter.get("aspect", "16:9"),
                out_file,
                default_cut_mode=chapter_defaults.get("cut_mode", "contiguous"),
                trim_level=trim_level,
            )
            chapter["rendered"] = True
            chapter["output_file"] = str(out_file.relative_to(WORKSPACE_ROOT))
            rendered.append(out_file)

        for short in manifest.get("shorts") or []:
            if only and short["id"] != only:
                continue
            item_idx += 1
            if progress:
                progress.update(item_idx, item=short["id"], message=short["title"][:50])

            safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in short["title"][:40])
            out_file = short_output_path(deliverables_dir, short)
            rel = out_file.relative_to(WORKSPACE_ROOT)
            print(f" Short {short['id']}: {short['title']} → {rel} [{short.get('cut_mode', 'contiguous')}]")

            trim_level = "off"
            if trim_enabled:
                trim_level = resolve_trim_level(
                    clip_target=short.get("target"),
                    clip_override=short.get("trim"),
                    manifest_default=manifest_trim_default,
                    project_default=short_defaults.get("default_trim"),
                )

            render_clip_entry(
                source,
                short,
                short.get("aspect", "9:16"),
                out_file,
                default_cut_mode=short_defaults.get("cut_mode", "contiguous"),
                trim_level=trim_level,
            )
            short["rendered"] = True
            short["output_file"] = str(out_file.relative_to(WORKSPACE_ROOT))
            rendered.append(out_file)

    if polish:
        import importlib.util

        spec = importlib.util.spec_from_file_location("auto_edit", BASE_DIR / "auto-edit.py")
        auto_edit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(auto_edit)

        words_path = BASE_DIR / "subtitles" / f"{stem}.words.json"
        for clip in rendered:
            polished = clip.with_name(clip.stem + "_polished.mp4")
            auto_edit.process_video(
                clip,
                polished,
                words_json_path=words_path if words_path.exists() else None,
            )

    manifest_out = plan_dir / "manifest.json"
    manifest_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f" Done → {deliverables_dir.relative_to(WORKSPACE_ROOT)} ({len(rendered)} clips)")
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Render all clips from manifest.json")
    parser.add_argument("--manifest", required=True, help="Path to approved manifest.json")
    parser.add_argument("--project", help="Project ID for pipeline.json defaults")
    parser.add_argument("--polish", action="store_true", help="Apply SFX + zoom after cut")
    parser.add_argument("--only", help="Render single short/chapter id (e.g. sh01)")
    parser.add_argument("--no-trim", action="store_true", help="Skip silence trim even if pipeline enables it")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    project_id = args.project
    if not project_id and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        project_id = manifest.get("series_id") or manifest.get("stem")

    from contextlib import nullcontext

    timer_ctx = nullcontext()
    if project_id:
        from pipeline_log import StageTimer

        timer_ctx = StageTimer(
            project_id,
            "render_shorts",
            message=str(manifest_path.name),
            artifact=str(manifest_path.parent),
        )

    with timer_ctx:
        render_manifest(
            manifest_path,
            polish=args.polish,
            only=args.only,
            project_id=project_id,
            skip_trim=args.no_trim,
        )


if __name__ == "__main__":
    main()
