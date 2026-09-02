#!/usr/bin/env python3
"""Per-project pipeline stage log — tracks stage, status, and elapsed time."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"

STAGES = [
    "discover",
    "concat",
    "trim_silence",
    "transcribe",
    "plan_shorts",
    "render_shorts",
    "polish",
    "done",
]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _now_local() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds: float) -> str:
    """Human-readable duration: 45s, 3m 12s, 1h 5m."""
    seconds = max(0, int(round(seconds)))
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {secs}s" if secs else f"{minutes}m"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m" if minutes else f"{hours}h"


def log_path(project_id: str) -> Path:
    return PROJECTS_DIR / project_id / "pipeline.log.json"


def timing_log_path(project_id: str) -> Path:
    return PROJECTS_DIR / project_id / "pipeline.timing.log"


def load_log(project_id: str) -> dict[str, Any]:
    path = log_path(project_id)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "project_id": project_id,
        "current_stage": None,
        "updated_at": _now(),
        "totals": {},
        "history": [],
    }


def save_log(project_id: str, data: dict[str, Any]) -> Path:
    path = log_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def append_timing_line(project_id: str, line: str) -> None:
    path = timing_log_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def _add_total(data: dict, stage: str, seconds: float) -> None:
    totals = data.setdefault("totals", {})
    totals[stage] = round(totals.get(stage, 0) + seconds, 1)


def log_stage(
    project_id: str,
    stage: str,
    status: str,
    *,
    message: str = "",
    artifact: str | None = None,
    details: dict | None = None,
    duration_seconds: float | None = None,
) -> Path:
    """
    Append a stage entry and set current_stage.

    status: started | done | failed | skipped
    duration_seconds: set on done/failed/skipped to record elapsed time
    """
    data = load_log(project_id)
    entry: dict[str, Any] = {
        "stage": stage,
        "status": status,
        "at": _now(),
        "message": message,
    }
    if artifact:
        entry["artifact"] = artifact
    if details:
        entry["details"] = details
    if duration_seconds is not None:
        entry["duration_seconds"] = round(duration_seconds, 1)
        entry["duration_human"] = format_duration(duration_seconds)
        if status in ("done", "failed", "skipped"):
            _add_total(data, stage, duration_seconds)

    data["history"].append(entry)
    if status == "started":
        data["current_stage"] = stage
    elif status == "failed":
        data["current_stage"] = stage

    path = save_log(project_id, data)

    # Plain-text timing log (easy to tail)
    dur = f"  ({format_duration(duration_seconds)})" if duration_seconds is not None else ""
    art = f"  → {artifact}" if artifact else ""
    msg = f"  {message}" if message else ""
    append_timing_line(
        project_id,
        f"{_now_local()}  {stage:<14} {status.upper():<7}{dur}{msg}{art}",
    )
    return path


class StageTimer:
    """Context manager: log started → work → log done/failed with elapsed time."""

    def __init__(
        self,
        project_id: str,
        stage: str,
        *,
        message: str = "",
        artifact: str | None = None,
    ):
        self.project_id = project_id
        self.stage = stage
        self.message = message
        self.artifact = artifact
        self._start: float | None = None

    def __enter__(self) -> StageTimer:
        self._start = time.monotonic()
        log_stage(self.project_id, self.stage, "started", message=self.message)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        elapsed = time.monotonic() - (self._start or time.monotonic())
        if exc_type is not None:
            log_stage(
                self.project_id,
                self.stage,
                "failed",
                message=str(exc),
                duration_seconds=elapsed,
            )
        else:
            log_stage(
                self.project_id,
                self.stage,
                "done",
                message=self.message,
                artifact=self.artifact,
                duration_seconds=elapsed,
            )


def print_status(project_id: str) -> None:
    data = load_log(project_id)
    print(f"Project: {project_id}")
    print(f"Current stage: {data.get('current_stage') or '—'}")
    print(f"Updated: {data.get('updated_at')}")

    totals = data.get("totals") or {}
    if totals:
        print("\nTotal time by stage:")
        for stage, secs in totals.items():
            print(f"  {stage:<14} {format_duration(secs)}")

    print("\nHistory (last 15):")
    for entry in data.get("history", [])[-15:]:
        dur = entry.get("duration_human") or ""
        if dur:
            dur = f" [{dur}]"
        art = f" → {entry['artifact']}" if entry.get("artifact") else ""
        msg = f" — {entry['message']}" if entry.get("message") else ""
        print(f"  [{entry['at']}] {entry['stage']} ({entry['status']}){dur}{msg}{art}")

    tlog = timing_log_path(project_id)
    if tlog.exists():
        print(f"\nTiming log: {tlog}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Project pipeline stage log")
    parser.add_argument("--project", required=True)
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--stage")
    parser.add_argument("--status", choices=["started", "done", "failed", "skipped"])
    parser.add_argument("--message", default="")
    parser.add_argument("--artifact")
    parser.add_argument("--duration", type=float, help="Duration in seconds (for done/failed)")
    args = parser.parse_args()

    if args.show:
        print_status(args.project)
    elif args.stage and args.status:
        log_stage(
            args.project,
            args.stage,
            args.status,
            message=args.message,
            artifact=args.artifact,
            duration_seconds=args.duration,
        )
        print_status(args.project)
    else:
        parser.print_help()
