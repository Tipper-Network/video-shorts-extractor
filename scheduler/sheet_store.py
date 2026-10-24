"""Read the publish catalog from Google Sheets. CSV is the offline fallback."""

from __future__ import annotations

import csv
import json
import os
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

WORKSPACE = Path(__file__).resolve().parents[1]
ENV_PATH = WORKSPACE / "integrations" / ".env"
CSV_PATH = WORKSPACE / "step-4-ready-to-post" / "publish_catalog.csv"
TOKEN_PATH = WORKSPACE / "step-5-google-sheets" / "credentials" / "sheets-token.json"
SNAPSHOT = Path(__file__).resolve().parent / "data" / "schedule.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]


def load_env() -> None:
    if not ENV_PATH.exists():
        return
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def _creds() -> Credentials:
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Missing Sheets token: {TOKEN_PATH}")
    data = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    creds = Credentials.from_authorized_user_info(data, scopes=data.get("scopes") or SCOPES)
    if not creds.valid:
        if not creds.refresh_token:
            raise RuntimeError("Sheets token expired and has no refresh token")
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return creds


def rows_from_csv() -> list[dict[str, str]]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rows_from_sheet() -> list[dict[str, str]]:
    load_env()
    sheet_id = os.environ.get("GOOGLE_SHEETS_ID", "").strip()
    tab = os.environ.get("GOOGLE_SHEETS_TAB", "publish_catalog").strip() or "publish_catalog"
    if not sheet_id:
        raise RuntimeError("GOOGLE_SHEETS_ID is not set")
    quoted = "'" + tab.replace("'", "''") + "'"
    service = build("sheets", "v4", credentials=_creds(), cache_discovery=False)
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=quoted)
        .execute()
    )
    values = result.get("values") or []
    if not values:
        return []
    header = [str(cell).strip() for cell in values[0]]
    rows: list[dict[str, str]] = []
    for raw in values[1:]:
        padded = list(raw) + [""] * (len(header) - len(raw))
        rows.append({header[i]: str(padded[i]).strip() for i in range(len(header))})
    return rows


_CACHE: dict[str, object] = {"at": 0.0, "rows": [], "source": "", "error": ""}


def load_rows(*, max_age: float = 30.0, force: bool = False) -> tuple[list[dict[str, str]], str, str]:
    """Return (rows, source, error). Source is 'sheet' or 'csv'."""
    now = time.time()
    if not force and _CACHE["rows"] and now - float(_CACHE["at"]) < max_age:
        return (
            list(_CACHE["rows"]),  # type: ignore[arg-type]
            str(_CACHE["source"]),
            str(_CACHE["error"]),
        )
    error = ""
    try:
        rows = rows_from_sheet()
        source = "sheet"
    except Exception as exc:  # noqa: BLE001 — show the failure on the page
        rows = rows_from_csv()
        source = "csv"
        error = str(exc)
    _CACHE["at"] = now
    _CACHE["rows"] = rows
    _CACHE["source"] = source
    _CACHE["error"] = error
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(
        json.dumps({"source": source, "error": error, "rows": rows}, indent=2),
        encoding="utf-8",
    )
    return rows, source, error
