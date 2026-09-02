#!/usr/bin/env python3
"""Batch-render chapters and shorts from an approved manifest.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cut_utils import render_clip_entry
from project_config import load_pipeline
from trim_profiles import resolve_trim_level

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def resolve_source(manifest: dict) -> Path:
    source = Path(manifest["source"])
    if source.is_absolute() and source.exists():
        return source
    for base in (BASE_DIR, BASE_DIR.parent):
        candidate = base / source
        if candidate.exists():
            return candidate
    return BASE_DIR.parent / source


def render_manifest(
    manifest_path: Path,
    polish: bool = False,
    only: str | None = None,
    project_id: str | None = None,
    skip_trim: bool = False,
) -> Path:
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    source = resolve_source(manifest)
    if not source.exists():
        print(f" Source not found: {source}")
        sys.exit(1)

    project_id = project_id or manifest.get("series_id") or manifest.get("stem")
    pipeline = load_pipeline(project_id) if project_id else {}
    render_cfg = pipeline.get("modules", {}).get("render", {})
    trim_enabled = render_cfg.get("trim_on_render", True) and not skip_trim

    chapter_defaults = pipeline.get("chapters", {})
    short_defaults = pipeline.get("shorts", {})

    stem = manifest["stem"]
    out_dir = OUTPUT_DIR / stem
    chapters_dir = out_dir / "chapters"
    shorts_dir = out_dir / "shorts"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    shorts_dir.mkdir(parents=True, exist_ok=True)

    manifest_trim_default = manifest.get("render", {}).get("default_trim")
    rendered = []

    for chapter in manifest.get("chapters") or []:
        if only and chapter["id"] != only:
            continue
        safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in chapter["title"][:40])
        out_file = chapters_dir / f"{chapter['id']}_{safe_title}.mp4"
        print(f" Chapter {chapter['id']}: {chapter['title']} [{chapter.get('cut_mode', 'contiguous')}]")

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
        chapter["output_file"] = str(out_file.relative_to(BASE_DIR.parent))
        rendered.append(out_file)

    for short in manifest.get("shorts") or []:
        if only and short["id"] != only:
            continue
        safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in short["title"][:40])
        out_file = shorts_dir / f"{short['id']}_{safe_title}.mp4"
        print(f" Short {short['id']}: {short['title']} [{short.get('cut_mode', 'contiguous')}]")

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
        short["output_file"] = str(out_file.relative_to(BASE_DIR.parent))
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

    manifest_out = out_dir / "manifest.json"
    manifest_out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f" Done → {out_dir} ({len(rendered)} clips)")
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Render all clips from manifest.json")
    parser.add_argument("--manifest", required=True, help="Path to approved manifest.json")
    parser.add_argument("--project", help="Project ID for pipeline.json defaults")
    parser.add_argument("--polish", action="store_true", help="Apply SFX + zoom after cut")
    parser.add_argument("--only", help="Render single short/chapter id (e.g. sh01)")
    parser.add_argument("--no-trim", action="store_true", help="Skip silence trim even if pipeline enables it")
    args = parser.parse_args()
    render_manifest(
        Path(args.manifest),
        polish=args.polish,
        only=args.only,
        project_id=args.project,
        skip_trim=args.no_trim,
    )


if __name__ == "__main__":
    main()
