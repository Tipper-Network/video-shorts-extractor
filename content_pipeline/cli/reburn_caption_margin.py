#!/usr/bin/env python3
"""Reburn stage1 captions at a new MarginV, then refresh stage2 → approved → step-4.

In-place only — no `_marginv*` copies. Cut masters under output/ are never touched.

  python3 content_pipeline/cli/reburn_caption_margin.py --margin 500
  python3 content_pipeline/cli/reburn_caption_margin.py --margin 500 --job 0
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
STEP2 = WORKSPACE / "step-2-viral-edit"
STEP4 = WORKSPACE / "step-4-ready-to-post"
SND = WORKSPACE / "content_pipeline" / "cli" / "viral_sounds.py"
ASSETS = WORKSPACE / "brands" / "assets"


def entity_for_job(name: str) -> str:
    low = name.lower()
    if "tipper" in low:
        return "tipper"
    if "gaf" in low or "qualifications" in low:
        return "gaf"
    if "origin story" in low or name.startswith("0."):
        return "founder"
    return "founder"


def fonts_dir(entity: str) -> Path:
    return ASSETS / entity / "fonts"


def set_ass_margin(ass: Path, margin: int) -> None:
    text = ass.read_text(encoding="utf-8")

    def bump(m: re.Match[str]) -> str:
        parts = m.group(0).split(",")
        parts[-2] = str(margin)
        return ",".join(parts)

    text2, n = re.subn(r"^Style: Body,.*$", bump, text, count=1, flags=re.M)
    if n != 1:
        raise RuntimeError(f"no Style: Body in {ass}")
    ass.write_text(text2, encoding="utf-8")


def clean_cut(job: Path, stem: str) -> Path | None:
    for sub in ("shorts_approved", "shorts"):
        p = job / "output" / "deliverables" / sub / f"{stem}.mp4"
        if p.is_file() and p.stat().st_size > 1000:
            return p
    return None


def words_path(stage1: Path, stem: str) -> Path | None:
    m = re.match(r"(sh\d+)", stem)
    sid = m.group(1) if m else stem
    for cand in (
        stage1 / f"{sid}_words.json",
        stage1 / f"{stem}_words.json",
    ):
        if cand.is_file():
            return cand
    return None


def burn(src: Path, ass: Path, fonts: Path, out: Path) -> None:
    ass_esc = str(ass).replace("\\", "/").replace(":", "\\:")
    fonts_esc = str(fonts).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-vf",
        f"ass={ass_esc}:fontsdir={fonts_esc}",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "copy",
        str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1200:])


def sync_step4(stem: str, approved: Path) -> int:
    """Copy approved → step-4 pack. Packs may be `{stem}.mp4` or `{nn}_{stem}.mp4`."""
    n = 0
    pat = re.compile(rf"^(?:\d+_)?{re.escape(stem)}\.mp4$")
    for dest in STEP4.rglob("*.mp4"):
        if dest.is_file() and pat.match(dest.name):
            shutil.copy2(approved, dest)
            n += 1
    return n


def process_ass(ass: Path, margin: int, *, dry: bool) -> str:
    stage1 = ass.parent
    job = stage1.parent.parent  # …/viral/stage1 → job
    stem = ass.stem
    entity = entity_for_job(job.name)
    fonts = fonts_dir(entity)
    src = clean_cut(job, stem)
    if not src:
        return f"SKIP no clean cut: {job.name}/{stem}"
    if not fonts.is_dir():
        return f"SKIP no fonts: {entity}"

    out1 = stage1 / f"{stem}.mp4"
    out2 = job / "viral" / "stage2" / f"{stem}.mp4"
    approved = job / "viral" / "approved" / f"{stem}.mp4"
    shorts_mirror = job / "viral" / "shorts" / f"{stem}.mp4"

    if dry:
        return f"DRY {job.name}/{stem} entity={entity} cut={src.name}"

    set_ass_margin(ass, margin)
    burn(src, ass, fonts, out1)

    words = words_path(stage1, stem)
    if words and SND.is_file():
        out2.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(
            [
                sys.executable,
                str(SND),
                "--input",
                str(out1),
                "--output",
                str(out2),
                "--words",
                str(words),
            ],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            return f"FAIL sounds {stem}: {r.stderr[-400:]}"
        ship = out2
    else:
        # No words → stage1 is the ship surface
        ship = out1
        if out2.parent.is_dir():
            shutil.copy2(out1, out2)

    approved.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ship, approved)
    if shorts_mirror.parent.is_dir():
        shutil.copy2(ship, shorts_mirror)

    n4 = sync_step4(stem, approved)
    return f"OK {job.name}/{stem} → stage2/approved + step4×{n4}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Reburn caption MarginV in place")
    ap.add_argument("--margin", type=int, default=500)
    ap.add_argument("--job", default="", help="Folder number prefix, e.g. 0 or 10")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=4, help="Parallel workers (default 4)")
    args = ap.parse_args()

    ass_files = sorted(
        p
        for p in STEP2.glob("*/viral/stage1/*.ass")
        if ".trash" not in str(p) and "_marginv" not in p.name
    )
    if args.job != "":
        ass_files = [
            p
            for p in ass_files
            if p.parts[-4].startswith(f"{args.job}.")
            or p.parts[-4] == args.job
        ]

    if args.limit:
        ass_files = ass_files[: args.limit]

    jobs = max(1, args.jobs)
    if args.dry_run:
        jobs = 1
    print(f"targets={len(ass_files)} margin={args.margin} dry={args.dry_run} jobs={jobs}")
    ok = fail = 0
    total = len(ass_files)

    def _one(ass: Path) -> str:
        return process_ass(ass, args.margin, dry=args.dry_run)

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futs = {pool.submit(_one, ass): ass for ass in ass_files}
        done_n = 0
        for fut in as_completed(futs):
            done_n += 1
            ass = futs[fut]
            try:
                msg = fut.result()
                print(f"[{done_n}/{total}] {msg}", flush=True)
                if msg.startswith("OK") or msg.startswith("DRY"):
                    ok += 1
                else:
                    fail += 1
            except Exception as e:
                fail += 1
                print(f"[{done_n}/{total}] FAIL {ass}: {e}", flush=True)
    print(f"done ok={ok} fail={fail}", flush=True)


if __name__ == "__main__":
    main()
