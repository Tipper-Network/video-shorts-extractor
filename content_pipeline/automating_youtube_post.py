#!/usr/bin/env python3
"""One-shot YouTube OAuth — uses Desktop client JSON under platforms/youtube/credentials/."""

from __future__ import annotations

import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

WORKSPACE = Path(__file__).resolve().parents[1]
CRED_DIR = WORKSPACE / "integrations" / "platforms" / "youtube" / "credentials"
TOKEN_OUT = CRED_DIR / "youtube-token.json"

# Prefer the downloaded OAuth client JSON; fall back to any client_secret_*.json
CLIENT_JSON_CANDIDATES = sorted(CRED_DIR.glob("client_secret_*.json"))

# upload alone often skips Brand Account channel picker → youtubeSignupRequired.
# youtube.force-ssl covers insert + update + thumbnails + channels.list(mine).
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
# Desktop clients often list only http://localhost — library picks an open port.
OAUTH_PORT = 8080


def main() -> None:
    if not CLIENT_JSON_CANDIDATES:
        raise SystemExit(
            f"No client_secret_*.json in {CRED_DIR}\n"
            "Download the Desktop OAuth client JSON from Google Cloud Console."
        )
    client_path = CLIENT_JSON_CANDIDATES[0]
    client_config = json.loads(client_path.read_text(encoding="utf-8"))
    if "installed" not in client_config and "web" not in client_config:
        raise SystemExit(f"Unexpected client JSON shape in {client_path}")

    print(f"Using OAuth client: {client_path.name}")
    print(f"Project: {client_config.get('installed', client_config.get('web', {})).get('project_id', '?')}")
    print(f"Scopes: {SCOPES}")
    print(f"Opening browser on http://localhost:{OAUTH_PORT}/ …")
    print("Sign in with the Google account that owns the YouTube channel.\n")

    flow = InstalledAppFlow.from_client_secrets_file(str(client_path), scopes=SCOPES)
    credentials = flow.run_local_server(
        port=OAUTH_PORT,
        prompt="consent",
        access_type="offline",
        open_browser=True,
    )

    TOKEN_OUT.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_OUT.write_text(credentials.to_json(), encoding="utf-8")

    print("\n" + "=" * 40)
    print("      AUTHENTICATION SUCCESSFUL!      ")
    print("=" * 40)
    print(f"Saved: {TOKEN_OUT}")
    has_refresh = bool(credentials.refresh_token)
    print(f"Refresh token: {'yes' if has_refresh else 'NO — re-run with prompt=consent'}")
    print("=" * 40 + "\n")
    print("Keep youtube-token.json private (gitignored). Ready for headless uploads.")


if __name__ == "__main__":
    main()
