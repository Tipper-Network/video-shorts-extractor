"""Load publish env from integrations/.env or workspace .env."""

from __future__ import annotations

import os
from pathlib import Path

from _root import WORKSPACE_ROOT


def _load_dotenv() -> None:
    """Load dotenv files. Later non-empty values win (so templates don't stick)."""
    for path in (
        WORKSPACE_ROOT / "integrations" / ".env",
        WORKSPACE_ROOT / ".env",
    ):
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if not key:
                continue
            prev = os.environ.get(key, "")
            if not prev or (val and prev.startswith("your_")):
                os.environ[key] = val
            elif val and not prev:
                os.environ[key] = val


def first(*keys: str, default: str = "") -> str:
    _load_dotenv()
    for k in keys:
        v = os.environ.get(k, "").strip()
        if v:
            return v
    return default


def dry_run() -> bool:
    return first("PUBLISH_DRY_RUN", default="true").lower() in ("1", "true", "yes")


def require_approved() -> bool:
    return first("PUBLISH_REQUIRE_APPROVED", default="true").lower() in (
        "1",
        "true",
        "yes",
    )
