"""Load content_pipeline/.env into os.environ (stdlib only)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_PIPELINE = Path(__file__).resolve().parents[1]
for _d in (_PIPELINE / "lib", _PIPELINE / "cli", _PIPELINE):
    _s = str(_d)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from _root import PIPELINE_ROOT  # noqa: E402

ENV_PATH = PIPELINE_ROOT / ".env"


def load_env() -> None:
    """Load ``content_pipeline/.env`` into ``os.environ``.

    Skips missing files, comments, and keys already set in the environment.
    """
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
