#!/usr/bin/env python3
"""Viral polish jobs 1–12 → step-3 queue → step-4 post packs.

Usage:
  python3 content_pipeline/cli/batch_to_step4.py            # viral + pack
  python3 content_pipeline/cli/batch_to_step4.py --packs-only
  python3 content_pipeline/cli/batch_to_step4.py --job 3    # one folder number
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
STEP2 = WORKSPACE / "step-2-viral-edit"
STEP3 = WORKSPACE / "step-3-flywheel-organiser"
STEP4 = WORKSPACE / "step-4-ready-to-post"
CAP = WORKSPACE / "content_pipeline" / "cli" / "viral_captions.py"
SND = WORKSPACE / "content_pipeline" / "cli" / "viral_sounds.py"

STAGE_BY_ORDER = {
    1: "attract",
    2: "engage",
    3: "trust",
    4: "service",
    5: "service",
    6: "referral",
    7: "referral",
    8: "loop",
    9: "loop",
}
STAGE_FOLDER = {
    "attract": "01-attract",
    "engage": "02-engage",
    "trust": "03-trust",
    "service": "04-service",
    "referral": "05-referral",
    "loop": "06-loop",
}
VIEWER = {
    "attract": "This is about me",
    "engage": "I want to respond",
    "trust": "This person is real",
    "service": "That helped me",
    "referral": "Others got results too",
    "loop": "I need what's next",
}
NEXT_STAGE = {
    "attract": "engage",
    "engage": "trust",
    "trust": "service",
    "service": "referral",
    "referral": "loop",
    "loop": "attract",
}


def series_meta(folder_name: str) -> tuple[str, str, str]:
    """Return (entity, series_slug, display)."""
    m = re.match(r"^(\d+)\.\s*(.+)$", folder_name) or re.match(
        r"^(\d+)\.(.+)$", folder_name
    )
    if not m:
        raise ValueError(folder_name)
    n = int(m.group(1))
    rest = m.group(2).strip()
    if n == 0:
        return "founder", "origin-story", rest
    if n >= 10:
        # The-GAF-qualifications 1 → qualifications-1
        slug = re.sub(r"[^a-z0-9]+", "-", rest.lower()).strip("-")
        slug = slug.replace("the-gaf-", "gaf-").replace("gaf-qualifications", "qualifications")
        if not slug.startswith("qualifications"):
            slug = f"qualifications-{n - 9}" if "qualifications" in slug else slug
        # normalize qualifications-1 / 2 / 3
        qm = re.search(r"qualifications[^\d]*(\d)", rest.lower())
        if qm:
            slug = f"qualifications-{qm.group(1)}"
        return "gaf", slug, rest
    slug = re.sub(r"[^a-z0-9]+", "-", rest.lower()).strip("-")
    return "tipper", slug, rest


def load_manifest_shorts(job: Path) -> dict[str, dict]:
    man = job / "output" / "plan" / "manifest.json"
    by_id: dict[str, dict] = {}
    if not man.exists():
        return by_id
    data = json.loads(man.read_text(encoding="utf-8"))
    for s in data.get("shorts", []):
        sid = s.get("id")
        if sid:
            by_id[sid] = s
    return by_id


def stem_id(stem: str) -> str:
    m = re.match(r"^(sh\d+)", stem)
    return m.group(1) if m else stem


def title_from_stem(stem: str) -> str:
    # sh02_island-bum_hook-first → Island Bum
    body = re.sub(r"^sh\d+_", "", stem)
    body = re.sub(r"_(hook-first|story-first|contiguous|v\d+)$", "", body)
    return body.replace("-", " ").replace("_", " ").strip().title()


def read_script_blurb(job: Path, stem: str) -> tuple[str, str]:
    """Return (problem_line, resolve_line) from script md if present."""
    md = job / "output" / "deliverables" / "shorts" / f"{stem}.md"
    problem = ""
    resolve = ""
    if not md.exists():
        return problem, resolve
    text = md.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if "**Problem**" in line or "| **Problem**" in line:
            problem = re.sub(r".*\|\s*", "", line).strip().strip("|").strip()
            # table cells: | **Problem** | text |
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                problem = parts[-1]
        if "**Resolve**" in line or "| **Resolve**" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                resolve = parts[-1]
    return problem, resolve


def ordered_entries(job: Path) -> list[dict]:
    shorts_dir = job / "output" / "deliverables" / "shorts"
    man = load_manifest_shorts(job)
    entries = []
    for mp4 in sorted(shorts_dir.glob("sh*.mp4")):
        stem = mp4.stem
        sid = stem_id(stem)
        meta = man.get(sid, {})
        order = meta.get("publish_order")
        # park huge orders at end but keep relative
        if isinstance(order, int) and order >= 90:
            order = 80 + (order - 90)
        stage = meta.get("flywheel_stage")
        title = meta.get("title") or title_from_stem(stem)
        entries.append(
            {
                "id": sid,
                "stem": stem,
                "mp4": mp4,
                "publish_order": order if isinstance(order, int) else 999,
                "flywheel_stage": stage,
                "title": title,
            }
        )
    entries.sort(key=lambda e: (e["publish_order"], e["id"]))
    # renumber sequential 1..n for shelf; fill missing stages
    for i, e in enumerate(entries, start=1):
        e["order"] = i
        if not e["flywheel_stage"]:
            e["flywheel_stage"] = STAGE_BY_ORDER.get(i, "service")
        e["problem"], e["resolve"] = read_script_blurb(job, e["stem"])
    return entries


def run_viral_one(job: Path, entity: str, entry: dict) -> Path:
    stem = entry["stem"]
    s1 = job / "viral" / "stage1"
    s2 = job / "viral" / "stage2"
    ap = job / "viral" / "approved"
    for d in (s1, s2, ap):
        d.mkdir(parents=True, exist_ok=True)

    out2 = s2 / f"{stem}.mp4"
    approved = ap / f"{stem}.mp4"
    if approved.exists() and approved.stat().st_size > 1000:
        print(f"  skip (approved): {stem}")
        return approved
    if out2.exists() and out2.stat().st_size > 1000:
        shutil.copy2(out2, approved)
        print(f"  promote stage2→approved: {stem}")
        return approved

    words = s1 / f"{entry['id']}_words.json"
    out1 = s1 / f"{stem}.mp4"
    if not out1.exists() or out1.stat().st_size < 1000:
        print(f"  stage1 captions: {stem}")
        cmd = [
            sys.executable,
            str(CAP),
            "--input",
            str(entry["mp4"]),
            "--output",
            str(out1),
            "--entity",
            entity,
            "--words-out",
            str(words),
        ]
        subprocess.run(cmd, check=True)
    else:
        print(f"  stage1 exists: {stem}")
        if not words.exists():
            # try alternate words path
            alt = s1 / f"{stem}_words.json"
            if alt.exists():
                words = alt

    print(f"  stage2 sounds: {stem}")
    cmd = [
        sys.executable,
        str(SND),
        "--input",
        str(out1),
        "--output",
        str(out2),
        "--words",
        str(words),
    ]
    subprocess.run(cmd, check=True)
    shutil.copy2(out2, approved)
    return approved


def hashtags_for(entity: str, series: str, title: str, stage: str) -> list[str]:
    theme = "#" + re.sub(r"[^A-Za-z0-9]+", "", title.title())[:28]
    tags = [theme]
    if entity == "tipper":
        tags += ["#Tipper", "#OneTipAtATime", "#BuildInPublic"]
    elif entity == "gaf":
        tags += ["#TheGAF", "#GuildOfGuilds", "#AssumptionsKillGrowth"]
    else:
        tags += ["#OriginStory", "#FounderLife", "#BuildInPublic"]
    tags.append("#" + series.replace("-", " ").title().replace(" ", ""))
    tags.append(f"#{stage.title()}")
    # dedupe preserve order
    seen = set()
    out = []
    for t in tags:
        if t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out[:8]


def write_pack_md(path: Path, *, entity: str, series: str, entry: dict) -> None:
    stage = entry["flywheel_stage"]
    title = entry["title"]
    problem = entry.get("problem") or title
    resolve = entry.get("resolve") or ""
    tags = hashtags_for(entity, series, title, stage)
    tag_line = " ".join(tags)
    viewer = VIEWER[stage]
    primes = NEXT_STAGE[stage]
    desc_lines = [problem, ""]
    if resolve:
        desc_lines += [resolve, ""]
    desc_lines += [
        f"Viewer state after: {viewer.lower()}.",
        f"Next in flywheel: {primes}.",
        "",
        tag_line,
    ]
    description = "\n".join(desc_lines)
    ig = f"{problem}\n\n{resolve}\n\n{tag_line}".strip() if resolve else f"{problem}\n\n{tag_line}"
    tt = f"{problem}\n\n{tag_line}"
    body = f"""---
entity: {entity}
series: {series}
stage: {stage}
order: {entry['order']}
kind: short
video: {entry['stem']}.mp4
viewer: "{viewer}"
primes: {primes}
product: cold
---

# {entry['id']} — {title}

## YouTube

**Title:**
{title}

**Description:**
{description}

**Tags:**
{title}, {series.replace('-', ' ')}, {entity}

## Instagram

**Caption:**
{ig}

## TikTok

**Caption:**
{tt}
"""
    path.write_text(body, encoding="utf-8")


def write_queues_and_packs(job: Path, entity: str, series: str, entries: list[dict]) -> None:
    qdir = STEP3 / entity / series
    qdir.mkdir(parents=True, exist_ok=True)
    (qdir / "queue").mkdir(exist_ok=True)

    queue_rows = []
    for e in entries:
        src = job / "viral" / "approved" / f"{e['stem']}.mp4"
        if not src.exists():
            src = job / "viral" / "stage2" / f"{e['stem']}.mp4"
        if not src.exists():
            print(f"  WARN missing viral for pack: {e['stem']}")
            continue
        qname = f"{e['order']:02d}_{e['stem']}.mp4"
        shutil.copy2(src, qdir / "queue" / qname)

        stage_folder = STAGE_FOLDER[e["flywheel_stage"]]
        shelf = STEP4 / entity / series / stage_folder
        shelf.mkdir(parents=True, exist_ok=True)
        # unique file name if multiple in same stage
        dest_mp4 = shelf / f"{e['order']:02d}_{e['stem']}.mp4"
        dest_md = shelf / f"{e['order']:02d}_{e['stem']}.md"
        shutil.copy2(src, dest_mp4)
        e_pack = dict(e)
        e_pack["stem"] = dest_mp4.stem  # include order prefix in frontmatter video name
        write_pack_md(dest_md, entity=entity, series=series, entry={**e, "stem": dest_mp4.stem})

        queue_rows.append(
            {
                "publish_order": e["order"],
                "id": e["id"],
                "slug": e["stem"].split("_", 1)[-1] if "_" in e["stem"] else e["stem"],
                "stem": e["stem"],
                "title": e["title"],
                "flywheel_stage": e["flywheel_stage"],
                "viewer_state": VIEWER[e["flywheel_stage"]],
                "next_stage": NEXT_STAGE[e["flywheel_stage"]],
                "file": f"queue/{qname}",
                "step4": str(shelf.relative_to(WORKSPACE)) + "/",
            }
        )

    payload = {
        "entity": entity,
        "series": series,
        "strategy": "flywheel-shorts",
        "source_job": str(job.relative_to(WORKSPACE)),
        "viral_source": "viral/approved",
        "queue": queue_rows,
    }
    (qdir / "publish_queue.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    readme = STEP4 / entity / series / "README.md"
    lines = [
        f"# {series} — ready to post",
        "",
        f"**Entity:** {entity} · **Series:** {series}",
        f"**Source:** `{payload['source_job']}`",
        "",
        "| Order | Stage | File |",
        "|------:|-------|------|",
    ]
    for r in queue_rows:
        lines.append(
            f"| {r['publish_order']} | {r['flywheel_stage']} | `{r['stem']}` |"
        )
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  packs: {len(queue_rows)} → step-4/{entity}/{series}/")


def process_job(job: Path, *, packs_only: bool) -> None:
    entity, series, _ = series_meta(job.name)
    print(f"\n======== {job.name} → {entity}/{series} ========")
    entries = ordered_entries(job)
    if not entries:
        print("  no shorts — skip")
        return
    if not packs_only:
        for e in entries:
            try:
                run_viral_one(job, entity, e)
            except subprocess.CalledProcessError as err:
                print(f"  FAIL viral {e['stem']}: {err}")
                continue
    write_queues_and_packs(job, entity, series, entries)


def list_jobs(only: int | None) -> list[Path]:
    jobs = []
    for p in sorted(STEP2.iterdir()):
        if not p.is_dir() or p.name.startswith("_"):
            continue
        m = re.match(r"^(\d+)", p.name)
        if not m:
            continue
        n = int(m.group(1))
        if n < 1 or n > 12:
            continue
        if only is not None and n != only:
            continue
        jobs.append(p)
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--packs-only", action="store_true")
    ap.add_argument("--job", type=int, default=None, help="Folder number 1–12")
    args = ap.parse_args()
    jobs = list_jobs(args.job)
    if not jobs:
        raise SystemExit("No jobs matched")
    for job in jobs:
        process_job(job, packs_only=args.packs_only)
    print("\nALL DONE")


if __name__ == "__main__":
    main()
