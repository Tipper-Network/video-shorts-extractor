#!/usr/bin/env python3
"""Push step-4 publish_catalog.csv → Google Sheet (full replace of tab values).

Auth: Desktop OAuth client under integrations/platforms/youtube/credentials/
(or step-5-google-sheets/credentials/oauth-client.json). First run opens browser
for Sheets scope; token saved to step-5-google-sheets/credentials/sheets-token.json.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

WORKSPACE = Path(__file__).resolve().parents[2]
ENV_PATH = WORKSPACE / "integrations" / ".env"
CSV_PATH = WORKSPACE / "step-4-ready-to-post" / "publish_catalog.csv"
CRED_DIR = WORKSPACE / "step-5-google-sheets" / "credentials"
TOKEN_PATH = CRED_DIR / "sheets-token.json"
YT_CLIENT = WORKSPACE / "integrations" / "platforms" / "youtube" / "credentials"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def client_secrets_path() -> Path:
    oauth = CRED_DIR / "oauth-client.json"
    if oauth.exists():
        return oauth
    cands = sorted(YT_CLIENT.glob("client_secret_*.json"))
    if cands:
        return cands[0]
    raise SystemExit(
        f"Need OAuth client JSON at {oauth} or {YT_CLIENT}/client_secret_*.json"
    )


def credentials() -> Credentials:
    CRED_DIR.mkdir(parents=True, exist_ok=True)
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_path()), scopes=SCOPES
        )
        creds = flow.run_local_server(port=8090, prompt="consent", access_type="offline")
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        print(f"Saved Sheets token: {TOKEN_PATH}")
    return creds


def main() -> None:
    load_env(ENV_PATH)
    sheet_id = os.environ.get("GOOGLE_SHEETS_ID", "").strip()
    tab = os.environ.get("GOOGLE_SHEETS_TAB", "publish_catalog").strip() or "publish_catalog"
    if not sheet_id:
        raise SystemExit("Set GOOGLE_SHEETS_ID in integrations/.env")
    if not CSV_PATH.exists():
        raise SystemExit(f"Missing {CSV_PATH}")

    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise SystemExit("Catalog CSV is empty")

    print(f"Pushing {len(rows) - 1} data rows + header → {sheet_id} / {tab}")
    print(f"Columns ({len(rows[0])}): {', '.join(rows[0])}")
    if "collaborators" not in rows[0]:
        print("WARN: collaborators column missing from CSV", file=sys.stderr)

    svc = build("sheets", "v4", credentials=credentials())
    # Quote tab title so names like publish_catalog / Sheet 1 parse
    tab_ref = f"'{tab.replace(chr(39), chr(39)+chr(39))}'"
    # Clear then write so removed columns don't linger
    svc.spreadsheets().values().clear(
        spreadsheetId=sheet_id, range=tab_ref
    ).execute()
    svc.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=f"{tab_ref}!A1",
        valueInputOption="RAW",
        body={"values": rows},
    ).execute()
    print(f"OK — Sheet updated (full tab replace → {tab}).")
    print(f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit")


if __name__ == "__main__":
    main()
