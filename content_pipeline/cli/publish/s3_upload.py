#!/usr/bin/env python3
"""Upload one (or more) local mp4s to the publish S3 bucket and print a presigned URL.

  python3 content_pipeline/cli/publish/s3_upload.py \\
    step-4-ready-to-post/founder/origin-story/03-trust/sh01_reaction-vs-response_story-first.mp4

  python3 content_pipeline/cli/publish/s3_upload.py --example
  python3 content_pipeline/cli/publish/s3_upload.py --force path/to/clip.mp4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PIPELINE = Path(__file__).resolve().parents[2]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from _root import WORKSPACE_ROOT  # noqa: E402
from publish.media_host import (  # noqa: E402
    object_key_for,
    public_url_for,
    s3_configured,
)
from publish.pack_caption import EXAMPLE_PACK_MP4  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Upload mp4 → S3 + print presigned GET URL")
    ap.add_argument("paths", nargs="*", type=Path, help="Local mp4 path(s)")
    ap.add_argument(
        "--example",
        action="store_true",
        help="Upload the IG reference pack (founder sh01)",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Re-upload even if same key+size already exists",
    )
    ap.add_argument(
        "--no-upload",
        action="store_true",
        help="Only print the key / presign for an assumed-existing object",
    )
    args = ap.parse_args()

    if not s3_configured():
        raise SystemExit(
            "S3 not configured — need AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "
            "and S3_URI (or S3_BUCKET) in integrations/.env"
        )

    paths: list[Path] = []
    if args.example:
        paths.append(WORKSPACE_ROOT / EXAMPLE_PACK_MP4)
    for p in args.paths:
        paths.append(p if p.is_absolute() else WORKSPACE_ROOT / p)

    if not paths:
        ap.error("pass mp4 path(s) or --example")

    for local in paths:
        if not local.is_file():
            print(f"MISSING {local}", file=sys.stderr)
            continue
        print(f"local={local}")
        print(f"key={object_key_for(local)}")
        url = public_url_for(
            local,
            upload=not args.no_upload,
            force_upload=args.force,
        )
        print(f"url={url}")
        print()


if __name__ == "__main__":
    main()
