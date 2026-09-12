#!/usr/bin/env python3
"""Per-project pipeline stage log — stages, elapsed time, and live % progress."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent
PROJECTS_DIR = WORKSPACE_ROOT / "projects"

STAGES = [
    "discover",
    "concat",
    "trim_silence",
    "transcribe",
    "detect_topics",
    "plan_shorts",
    "plan_manifest",
    "compose_shorts",
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
    from project_config import find_project_dir

    return find_project_dir(project_id) / "pipeline.log.json"


def timing_log_path(project_id: str) -> Path:
    from project_config import find_project_dir

    return find_project_dir(project_id) / "pipeline.timing.log"


def progress_path(project_id: str) -> Path:
    from project_config import find_project_dir

    return find_project_dir(project_id) / "pipeline.progress.json"


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


def load_progress(project_id: str) -> dict[str, Any] | None:
    path = progress_path(project_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_log(project_id: str, data: dict[str, Any]) -> Path:
    path = log_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def save_progress(project_id: str, data: dict[str, Any]) -> Path:
    path = progress_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = _now()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def clear_progress(project_id: str) -> None:
    path = progress_path(project_id)
    if path.exists():
        path.unlink()


def append_timing_line(project_id: str, line: str) -> None:
    path = timing_log_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def _add_total(data: dict, stage: str, seconds: float) -> None:
    totals = data.setdefault("totals", {})
    totals[stage] = round(totals.get(stage, 0) + seconds, 1)


def _estimate_eta(elapsed: float, current: int, total: int) -> float | None:
    if current <= 0 or total <= 0 or current >= total:
        return None
    return elapsed / current * (total - current)


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

    status: started | done | failed | skipped | progress
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
    elif status in ("failed", "progress"):
        data["current_stage"] = stage
    elif status == "done":
        data["current_stage"] = stage

    path = save_log(project_id, data)

    dur = f"  ({format_duration(duration_seconds)})" if duration_seconds is not None else ""
    art = f"  → {artifact}" if artifact else ""
    msg = f"  {message}" if message else ""
    append_timing_line(
        project_id,
        f"{_now_local()}  {stage:<14} {status.upper():<7}{dur}{msg}{art}",
    )
    return path


def log_progress(
    project_id: str,
    stage: str,
    current: int,
    total: int,
    *,
    unit: str = "item",
    item: str = "",
    message: str = "",
    started_at: float | None = None,
) -> dict[str, Any]:
    """Write live progress snapshot + append timing line with % and ETA."""
    if started_at is None:
        started_at = time.monotonic()
    elapsed = time.monotonic() - started_at
    percent = round(min(100.0, (current / total * 100) if total else 0), 1)
    eta = _estimate_eta(elapsed, current, total)

    snapshot: dict[str, Any] = {
        "project_id": project_id,
        "stage": stage,
        "status": "running",
        "started_at": _now(),
        "current": current,
        "total": total,
        "percent": percent,
        "unit": unit,
        "item": item,
        "message": message,
        "elapsed_seconds": round(elapsed, 1),
        "elapsed_human": format_duration(elapsed),
    }
    if eta is not None:
        snapshot["eta_seconds"] = round(eta, 1)
        snapshot["eta_human"] = format_duration(eta)

    save_progress(project_id, snapshot)

    pct = f"{percent:5.1f}%"
    count = f"{current}/{total}"
    el = format_duration(elapsed)
    eta_str = f"  ETA ~{format_duration(eta)}" if eta is not None else ""
    item_str = f"  {item}" if item else ""
    msg = f"  {message}" if message else ""
    append_timing_line(
        project_id,
        f"{_now_local()}  {stage:<14} {'PROGRESS':<7}  {pct}  {count}  elapsed {el}{eta_str}{item_str}{msg}",
    )
    return snapshot


class ProgressTracker:
    """Track sub-step progress within a stage (% complete + ETA)."""

    def __init__(
        self,
        project_id: str,
        stage: str,
        total: int,
        *,
        unit: str = "item",
        message: str = "",
    ):
        self.project_id = project_id
        self.stage = stage
        self.total = max(total, 1)
        self.unit = unit
        self.message = message
        self._start = time.monotonic()
        self._current = 0

    def update(
        self,
        current: int,
        *,
        item: str = "",
        message: str = "",
    ) -> dict[str, Any]:
        self._current = current
        return log_progress(
            self.project_id,
            self.stage,
            current,
            self.total,
            unit=self.unit,
            item=item,
            message=message or self.message,
            started_at=self._start,
        )

    def step(self, *, item: str = "", message: str = "") -> dict[str, Any]:
        return self.update(self._current + 1, item=item, message=message)

    def finish(self, *, message: str = "") -> None:
        log_progress(
            self.project_id,
            self.stage,
            self.total,
            self.total,
            unit=self.unit,
            message=message or "complete",
            started_at=self._start,
        )
        snap = load_progress(self.project_id) or {}
        snap["status"] = "complete"
        snap["percent"] = 100.0
        save_progress(self.project_id, snap)

    def __enter__(self) -> ProgressTracker:
        log_progress(
            self.project_id,
            self.stage,
            0,
            self.total,
            unit=self.unit,
            message=self.message or "starting",
            started_at=self._start,
        )
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            snap = load_progress(self.project_id) or {}
            snap["status"] = "failed"
            snap["error"] = str(exc)
            save_progress(self.project_id, snap)
        else:
            self.finish()


class StageTimer:
    """Context manager: log started → work → log done/failed with elapsed time."""

    def __init__(
        self,
        project_id: str,
        stage: str,
        *,
        message: str = "",
        artifact: str | None = None,
        total: int | None = None,
        unit: str = "item",
    ):
        self.project_id = project_id
        self.stage = stage
        self.message = message
        self.artifact = artifact
        self.total = total
        self.unit = unit
        self._start: float | None = None
        self.progress: ProgressTracker | None = None

    def __enter__(self) -> StageTimer:
        self._start = time.monotonic()
        log_stage(self.project_id, self.stage, "started", message=self.message)
        if self.total is not None:
            self.progress = ProgressTracker(
                self.project_id,
                self.stage,
                self.total,
                unit=self.unit,
                message=self.message,
            )
            self.progress.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.progress is not None:
            if exc_type is not None:
                self.progress.__exit__(exc_type, exc, tb)
            else:
                self.progress.finish()
            clear_progress(self.project_id)

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

    prog = load_progress(project_id)
    if prog and prog.get("status") == "running":
        eta = prog.get("eta_human") or "—"
        print(
            f"\nLive progress: {prog.get('percent', 0):.1f}%  "
            f"({prog.get('current')}/{prog.get('total')} {prog.get('unit', 'item')})  "
            f"elapsed {prog.get('elapsed_human', '—')}  ETA ~{eta}"
        )
        if prog.get("item"):
            print(f"  Current: {prog['item']}")
        if prog.get("message"):
            print(f"  {prog['message']}")

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
        print(f"Progress snapshot: {progress_path(project_id)}")


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
    parser.add_argument("--progress", action="store_true", help="Log progress tick (needs --current --total)")
    parser.add_argument("--current", type=int)
    parser.add_argument("--total", type=int)
    parser.add_argument("--unit", default="item")
    parser.add_argument("--item", default="")
    args = parser.parse_args()

    if args.show:
        print_status(args.project)
    elif args.progress and args.stage and args.current is not None and args.total is not None:
        log_progress(
            args.project,
            args.stage,
            args.current,
            args.total,
            unit=args.unit,
            item=args.item,
            message=args.message,
        )
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
