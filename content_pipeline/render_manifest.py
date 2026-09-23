#!/usr/bin/env python3
"""Batch-render chapters and shorts from an approved manifest.json."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from pathlib import Path

from cut_utils import render_clip_entry
from project_config import load_pipeline
from project_paths import load_project_paths
from trim_profiles import resolve_trim_level

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent

def resolve_short_versions(short: dict) -> list[dict]:
    """Editorial versions of one short (not platforms).

    Args:
        short: Manifest short dict.

    Returns:
        ``short["versions"]``, or ``[short]`` if none.
    """
    versions = short.get("versions")
    if versions:
        return list(versions)
    return [short]


def short_output_path(deliverables_dir: Path, short: dict, version: dict, safe_title: str | None = None) -> Path:
    """Destination under ``deliverables/shorts/`` for one editorial version.

    Args:
        deliverables_dir: Project deliverables root.
        short: Parent short dict.
        version: Version dict (or the short itself).
        safe_title: Fallback slug when no ``output_name``.

    Returns:
        ``.mp4`` path (file may not exist yet).
    """
    subdir = deliverables_dir / "shorts"
    subdir.mkdir(parents=True, exist_ok=True)

    base_name = version.get("output_name") or short.get("output_name")
    if not base_name:
        slug = safe_title.lower() if safe_title else "clip"
        base_name = f"{short['id']}_{slug}"

    if base_name.endswith(".mp4"):
        base_name = base_name[:-4]

    version_id = version.get("version_id") or version.get("id")
    if version_id and version is not short and version_id != short.get("id"):
        name = f"{base_name}_{version_id}.mp4"
    else:
        name = f"{base_name}.mp4"
    return subdir / name


def promote_to_approved(src: Path, deliverables_dir: Path) -> Path:
    """Copy a finished short into ``shorts_approved/``. Never overwrites an approved file.

    Args:
        src: Rendered draft mp4.
        deliverables_dir: Project deliverables root.

    Returns:
        Path in ``shorts_approved/`` (``_vN`` if the name was taken).
    """
    approved = deliverables_dir / "shorts_approved"
    approved.mkdir(parents=True, exist_ok=True)
    dest = approved / src.name
    if dest.exists():
        dest = compare_output_path(dest)
    shutil.copy2(src, dest)
    print(f" Promoted → {dest.relative_to(WORKSPACE_ROOT)}")
    return dest


def compare_output_path(dest: Path, *, overwrite: bool = False) -> Path:
    """Keep an existing render so the next pass can be A/B'd.

    Never clobber ``dest`` or an existing ``_vN``.

    Args:
        dest: Intended output path.
        overwrite: If True, return ``dest`` (in-place replace).

    Returns:
        ``dest`` if free (or overwrite), else the next free ``{stem}_vN.mp4``.
    """
    import re

    if overwrite:
        return dest
    base = re.sub(r"_v\d+$", "", dest.stem)
    if not dest.exists():
        # dest is free, but don't land on an orphan _vN name either
        return dest
    n = 2
    while True:
        candidate = dest.with_name(f"{base}_v{n}{dest.suffix}")
        if not candidate.exists():
            print(f" Keeping {dest.name} — writing {candidate.name} for compare")
            return candidate
        n += 1


def chapter_output_path(deliverables_dir: Path, chapter: dict) -> Path:
    """Destination under ``deliverables/chunks/``.

    Args:
        deliverables_dir: Project deliverables root.
        chapter: Manifest chapter dict.

    Returns:
        ``.mp4`` path.
    """
    subdir = deliverables_dir / "chunks"
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
    """Resolve ``manifest["source"]`` against the project, pipeline dir, or workspace.

    Args:
        manifest: Loaded manifest.
        project_id: Optional project for a search root.

    Returns:
        Existing file if found; otherwise ``workspace / source`` (may be missing).
    """
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
    overwrite: bool = False,
    **kwargs,
) -> Path:
    """Batch-render chapters and/or shorts from an approved manifest.

    Args:
        manifest_path: ``output/plan/manifest.json``.
        polish: Run auto-edit (SFX + zoom) after the cut.
        only: Render this clip id only (``sh01``, ``ch01``, …).
        project_id: Pipeline defaults / path root.
        skip_trim: Do not apply silence trim even if the pipeline wants it.
        overwrite: Replace existing files instead of writing ``_vN``.
        **kwargs: Extra CLI flags forwarded from ``main`` (``jobs``, ``type``, …).

    Returns:
        Deliverables directory used.
    """
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
    render_type = kwargs.get("render_type")
    
    for chapter in manifest.get("chapters") or []:
        if only and chapter["id"] != only:
            continue
        if render_type and render_type != "chapters":
            continue
        work_items.append(("chapter", chapter, "16:9"))
        
    for short in manifest.get("shorts") or []:
        if only and short["id"] != only:
            continue
        if render_type and render_type != "shorts":
            continue
        only_version = kwargs.get("only_version")
        for version in resolve_short_versions(short):
            version_id = version.get("version_id") or version.get("id") or short["id"]
            if only_version and version_id != only_version:
                continue
            work_items.append(("short", short, version_id))

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
            if render_type and render_type != "chapters":
                continue
            item_idx += 1
            if progress:
                progress.update(item_idx, item=chapter["id"], message=chapter["title"][:50])

            out_file = compare_output_path(
                chapter_output_path(deliverables_dir, chapter),
                overwrite=overwrite,
            )
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

        short_jobs: list[dict] = []
        for short in manifest.get("shorts") or []:
            if only and short["id"] != only:
                continue
            if render_type and render_type != "shorts":
                continue
            versions = resolve_short_versions(short)
            only_version = kwargs.get("only_version")
            if only_version:
                versions = [
                    v
                    for v in versions
                    if (v.get("version_id") or v.get("id")) == only_version
                ]
                if not versions:
                    print(f" No version {only_version!r} on {short['id']}")
                    continue
            safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in short["title"][:40])
            short["output_files"] = {}

            for version in versions:
                clip = {**short, **version} if version is not short else short
                version_id = version.get("version_id") or version.get("id") or short["id"]

                approved = version.get("script_approved", short.get("script_approved", True))
                if approved is False and not kwargs.get("allow_unapproved"):
                    print(
                        f" Skip {short['id']} [{version_id}]: script not approved — "
                        "paste spoken_as and wait"
                    )
                    continue

                out_file = compare_output_path(
                    short_output_path(deliverables_dir, short, version, safe_title=safe_title),
                    overwrite=overwrite,
                )
                if out_file.exists() and not overwrite:
                    out_file = compare_output_path(out_file, overwrite=False)
                trim_level = "off"
                if trim_enabled:
                    trim_level = resolve_trim_level(
                        clip_target="short",
                        clip_override=clip.get("trim"),
                        manifest_default=manifest_trim_default,
                        project_default=short_defaults.get("default_trim"),
                    )
                short_jobs.append(
                    {
                        "short": short,
                        "clip": clip,
                        "version_id": version_id,
                        "out_file": out_file,
                        "trim_level": trim_level,
                    }
                )

        jobs = max(1, int(kwargs.get("jobs") or 4))
        progress_lock = threading.Lock()

        def _run_short(job: dict) -> Path:
            out_file = job["out_file"]
            clip = job["clip"]
            short = job["short"]
            rel = out_file.relative_to(WORKSPACE_ROOT)
            print(
                f" Short {short['id']} [{job['version_id']}]: {short['title']} → {rel}"
                f" [{clip.get('cut_mode', 'contiguous')}]"
            )
            render_clip_entry(
                source,
                clip,
                clip.get("aspect", "9:16"),
                out_file,
                default_cut_mode=short_defaults.get("cut_mode", "contiguous"),
                trim_level=job["trim_level"],
            )
            return out_file

        if short_jobs:
            print(f" Shorts: {len(short_jobs)} clips, {min(jobs, len(short_jobs))} in parallel")
            with ThreadPoolExecutor(max_workers=min(jobs, len(short_jobs))) as pool:
                futures = {pool.submit(_run_short, job): job for job in short_jobs}
                for fut in as_completed(futures):
                    job = futures[fut]
                    out_file = fut.result()
                    job["short"]["output_files"][job["version_id"]] = str(
                        out_file.relative_to(WORKSPACE_ROOT)
                    )
                    rendered.append(out_file)
                    with progress_lock:
                        item_idx += 1
                        if progress:
                            progress.update(
                                item_idx,
                                item=f"{job['short']['id']}:{job['version_id']}",
                                message=f"{job['short']['title'][:40]} [{job['version_id']}]",
                            )

        for short in manifest.get("shorts") or []:
            if only and short["id"] != only:
                continue
            if render_type and render_type != "shorts":
                continue
            if short.get("output_files"):
                short["rendered"] = True
                short["output_file"] = next(iter(short["output_files"].values()))

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
    """CLI: render shorts/chapters from ``manifest.json`` (``--project`` or ``--manifest``)."""
    parser = argparse.ArgumentParser(description="Render all clips from manifest.json")
    parser.add_argument("--manifest", help="Path to approved manifest.json")
    parser.add_argument("--project", help="Project ID for pipeline.json defaults")
    parser.add_argument("--polish", action="store_true", help="Apply SFX + zoom after cut")
    parser.add_argument("--only", help="Render single short/chapter id (e.g. sh01)")
    parser.add_argument("--version", help="Render one editorial version (e.g. story-first)")
    parser.add_argument("--type", choices=["shorts", "chapters"], help="Filter by type")
    parser.add_argument(
        "--jobs",
        type=int,
        default=4,
        help="Parallel ffmpeg workers for shorts (default: 4). Chapters stay serial.",
    )
    parser.add_argument("--no-trim", action="store_true", help="Skip silence trim even if pipeline enables it")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the existing file instead of writing a _v2 / _v3 compare copy",
    )
    parser.add_argument(
        "--promote",
        help="Copy an existing short .mp4 into deliverables/shorts_approved/ (no re-encode)",
    )
    args = parser.parse_args()

    if args.promote:
        src = Path(args.promote)
        if not src.is_absolute():
            src = WORKSPACE_ROOT / src
        if not src.exists():
            print(f" Not found: {src}")
            sys.exit(1)
        project_id = args.project
        paths = load_project_paths(project_id) if project_id else None
        dest_root = paths.deliverables_dir if paths else src.parent.parent
        promote_to_approved(src, dest_root)
        return

    if not args.manifest:
        print(" --manifest is required unless using --promote")
        sys.exit(1)

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
            overwrite=args.force,
            render_type=args.type,
            only_version=args.version,
            jobs=args.jobs,
        )


if __name__ == "__main__":
    main()
