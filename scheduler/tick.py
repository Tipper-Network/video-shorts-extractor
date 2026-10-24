#!/usr/bin/env python3
"""Clock tick. Pull the Sheet, print due rows. Does not post.

Posting stays behind an explicit later step. A row is due only when
status=scheduled and scheduled_date <= today in Asia/Beirut.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from due import is_due, today  # noqa: E402
from sheet_store import load_rows  # noqa: E402


def main() -> None:
    rows, source, error = load_rows(force=True)
    day = today()
    due = [row for row in rows if is_due(row, now=day)]
    print(f"source={source} rows={len(rows)} today={day.isoformat()} due={len(due)}")
    if error:
        print(f"error={error}")
    for row in due:
        title = row.get("youtube_title") or row.get("title") or row.get("id")
        print(
            f"  DUE {row.get('scheduled_date')} {row.get('entity')} "
            f"{row.get('series')} {row.get('id')} {title}"
        )
    if not due:
        print("nothing scheduled for the clock")


if __name__ == "__main__":
    main()
