#!/usr/bin/env python3
"""Publish approved catalog rows to Instagram Reels (Graph API).

Reads step-4 publish_catalog.csv (or a path you pass).
Caption preference: pack ``## Instagram`` → **Caption:** block from ``md_path``.

Reference pack (credentials / first live post):
  step-4-ready-to-post/founder/origin-story/03-trust/sh01_reaction-vs-response_story-first.md

Requires public video URLs — see integrations/platforms/instagram/README.md.
Creates containers with share_to_feed=false by default (Reels tab only).

  # Dry-run the reference pack with your credentials:
  PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --example

  PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --limit 1
  PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --due-only --limit 1
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

_PIPELINE = Path(__file__).resolve().parents[2]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from _root import WORKSPACE_ROOT  # noqa: E402
from publish.env import dry_run, require_approved  # noqa: E402
from publish.instagram import (  # noqa: E402
    InstagramConfigError,
    list_collaborators,
    publish_reel_from_url,
)
from publish.media_host import public_url_for  # noqa: E402
from publish.pack_caption import (  # noqa: E402
    EXAMPLE_PACK_MD,
    EXAMPLE_PACK_MP4,
    caption_from_pack,
)

DEFAULT_CATALOG = WORKSPACE_ROOT / "step-4-ready-to-post" / "publish_catalog.csv"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def caption_for(row: dict[str, str]) -> str:
    """Prefer pack ## Instagram caption; fall back to catalog fields."""
    md_rel = (row.get("md_path") or "").strip()
    if md_rel:
        md = WORKSPACE_ROOT / md_rel
        if md.is_file():
            pack_cap = caption_from_pack(md, "instagram")
            if pack_cap:
                return pack_cap

    title = row.get("youtube_title") or row.get("title") or ""
    tags = row.get("hashtags") or ""
    desc = (row.get("description") or "").strip()
    parts = [title]
    if desc and len(desc) < 400:
        parts.append(desc)
    if tags:
        parts.append(tags)
    return "\n\n".join(p for p in parts if p).strip()


def example_row() -> dict[str, str]:
    """Canonical credential test: founder Origin Story sh01 (trust)."""
    return {
        "entity": "founder",
        "series": "origin-story",
        "id": "sh01",
        "status": "approved",
        "scheduled_date": date.today().isoformat(),
        "video_path": EXAMPLE_PACK_MP4,
        "md_path": EXAMPLE_PACK_MD,
        "youtube_title": "What if there's a 5% chance I'm an idiot?",
        "hashtags": "#ReactionVsResponse #OriginStory #SelfHonesty #FounderLife",
    }

def eligible(
    row: dict[str, str],
    *,
    today: date,
    due_only: bool,
    ignore_schedule: bool = False,
) -> bool:
    if require_approved() and (row.get("status") or "").strip().lower() not in (
        "approved",
        "scheduled",
    ):
        # In dry_run allow ready so you can inspect the queue
        if dry_run() and (row.get("status") or "").strip().lower() == "ready":
            pass
        else:
            return False
    if due_only and not ignore_schedule:
        sched = (row.get("scheduled_date") or "").strip()
        if not sched or sched > today.isoformat():
            return False
    if not (row.get("video_path") or "").strip():
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="IG Reels from publish catalog")
    ap.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    ap.add_argument("--limit", type=int, default=0, help="Max posts this run (0=all eligible)")
    ap.add_argument("--entity", default="", help="Filter entity tipper|gaf|founder")
    ap.add_argument("--series", default="", help="Filter series e.g. ig-test")
    ap.add_argument(
        "--id",
        default="",
        help="Filter catalog id e.g. sh01",
    )
    ap.add_argument(
        "--due-only",
        action="store_true",
        help="Only scheduled_date <= today",
    )
    ap.add_argument(
        "--ignore-schedule",
        action="store_true",
        help="Publish even if scheduled_date is in the future",
    )
    ap.add_argument(
        "--throttle",
        type=int,
        default=60,
        help="Seconds between publishes (IG throttle; default 60)",
    )
    ap.add_argument(
        "--share-to-feed",
        action="store_true",
        help="Also put Reel on the main profile grid (default: off / Reels tab only)",
    )
    ap.add_argument(
        "--example",
        action="store_true",
        help=(
            "Publish/dry-run only the reference pack: "
            "founder/origin-story/03-trust/sh01_reaction-vs-response_story-first"
        ),
    )
    args = ap.parse_args()

    today = date.today()
    if args.example:
        picked = [example_row()]
    else:
        rows = load_rows(args.catalog)
        picked = []
        for row in rows:
            if args.entity and row.get("entity") != args.entity:
                continue
            if args.series and row.get("series") != args.series:
                continue
            if args.id and row.get("id") != args.id:
                continue
            if not eligible(
                row,
                today=today,
                due_only=args.due_only,
                ignore_schedule=args.ignore_schedule,
            ):
                continue
            picked.append(row)
        if args.limit:
            picked = picked[: args.limit]
    print(f"catalog={args.catalog}")
    print(f"eligible={len(picked)} dry_run={dry_run()}")

    for i, row in enumerate(picked, 1):
        local = WORKSPACE_ROOT / row["video_path"]
        cap = caption_for(row)
        label = f"{row.get('entity')}/{row.get('series')}/{row.get('id')}"
        print(f"\n[{i}/{len(picked)}] {label} {row.get('scheduled_date')} {local.name}")

        share_to_feed = bool(args.share_to_feed)

        if dry_run():
            # Still hit S3 when configured so dry-run proves upload+presign.
            try:
                url = public_url_for(local, upload=True)
            except Exception as e:
                url = f"<no public url yet: {e}>"
            collabs = list_collaborators()
            print(f"  DRY caption={cap[:80]!r}…")
            print(f"  DRY video_url={url}")
            print(f"  DRY share_to_feed={share_to_feed}")
            print(f"  DRY collaborators={collabs or '(none)'}")
            continue

        try:
            url = public_url_for(local, upload=True)
            media_id = publish_reel_from_url(
                video_url=url,
                caption=cap,
                throttle_seconds=args.throttle,
                share_to_feed=share_to_feed,
            )
            print(f"  published media_id={media_id}")
        except InstagramConfigError as e:
            print(f"  CONFIG: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print("\ndone")


if __name__ == "__main__":
    main()
