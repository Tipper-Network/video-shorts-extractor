"""Which Sheet rows the clock is allowed to post."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Beirut")


def today() -> date:
    return datetime.now(TZ).date()


def is_due(row: dict[str, str], *, now: date | None = None) -> bool:
    """Due only when a human set status=scheduled and the date has arrived.

    `approved` and `ready` never fire. Time-of-day is ignored until the
    catalog grows a scheduled_time column.
    """
    status = (row.get("status") or "").strip().lower()
    if status != "scheduled":
        return False
    sched = (row.get("scheduled_date") or "").strip()
    if not sched:
        return False
    day = now or today()
    return sched <= day.isoformat()
