#!/usr/bin/env python3
"""One-shot YouTube OAuth — uses Desktop client JSON under platforms/youtube/credentials/."""

from __future__ import annotations

import json
import threading
import wsgiref.simple_server
import wsgiref.util
from pathlib import Path
from urllib.parse import parse_qs

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


def wait_for_browser(flow: InstalledAppFlow, port: int):
    """Listen on IPv4 and IPv6 until Google redirects back with a code.

    The stock helper listens on 127.0.0.1 only, holds ::1 without accepting
    connections, and exits on the first request. A browser that opens
    localhost over IPv6, or a cancelled attempt before approval, then shows
    "localhost refused to connect" on the real redirect.
    """

    class App:
        def __init__(self) -> None:
            self.uri: str | None = None
            self.expected_state = ""
            self.got_code = threading.Event()

        def __call__(self, environ, start_response):
            query = environ.get("QUERY_STRING", "")
            params = parse_qs(query)
            start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
            state = (params.get("state") or [""])[0]
            code = (params.get("code") or [""])[0]
            if not code or state != self.expected_state:
                print("Ignored an old or empty callback. Still waiting for this sign-in.")
                return [b"This tab is from an older sign-in. Close it and use the new URL."]
            self.uri = wsgiref.util.request_uri(environ)
            self.got_code.set()
            return [b"YouTube login received. You can close this tab."]

    app = App()
    servers: list[wsgiref.simple_server.WSGIServer] = []

    def serve(host: str) -> None:
        try:
            httpd = wsgiref.simple_server.make_server(host, port, app)
        except OSError as exc:
            print(f"Could not listen on {host}:{port}: {exc}")
            return
        servers.append(httpd)
        print(f"Listening on {host}:{port}")
        httpd.serve_forever()

    for host in ("127.0.0.1", "::1"):
        threading.Thread(target=serve, args=(host,), daemon=True).start()

    threading.Event().wait(0.4)
    if not servers:
        raise SystemExit(f"Port {port} is not available.")

    flow.redirect_uri = f"http://localhost:{port}/"
    auth_url, state = flow.authorization_url(
        prompt="consent select_account",
        access_type="offline",
        login_hint="gaf.chronicles@gmail.com",
    )
    app.expected_state = state
    print("\nOpen this URL in the browser where you can choose gaf.chronicles@gmail.com:")
    print(auth_url)
    print("\nLeave this running until it prints AUTHENTICATION SUCCESSFUL.")
    print("Do not reuse an older localhost tab. That code belongs to a listener that already quit.\n")

    if not app.got_code.wait(timeout=600):
        raise SystemExit("Timed out after 10 minutes.")

    for httpd in servers:
        httpd.shutdown()
    assert app.uri is not None
    flow.fetch_token(authorization_response=app.uri.replace("http", "https", 1))
    return flow.credentials


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
    credentials = wait_for_browser(flow, OAUTH_PORT)

    TOKEN_OUT.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_OUT.write_text(credentials.to_json(), encoding="utf-8")

    print("\n" + "=" * 40)
    print("      AUTHENTICATION SUCCESSFUL!      ")
    print("=" * 40)
    print(f"Saved: {TOKEN_OUT}")
    has_refresh = bool(credentials.refresh_token)
    print(f"Refresh token: {'yes' if has_refresh else 'NO — re-run with prompt=consent'}")

    # Brand Account must be selected during consent or mine=True is empty and uploads 401.
    try:
        from googleapiclient.discovery import build

        youtube = build("youtube", "v3", credentials=credentials)
        items = youtube.channels().list(part="snippet", mine=True).execute().get("items") or []
        if not items:
            print("CHANNEL: NONE — you did not pick The G.A.F. Brand Account.")
            print("Re-run and choose The G.A.F. (Guilds Adventurers and Frontiers) when Google asks.")
            print("Uploads will fail with youtubeSignupRequired until that happens.")
        else:
            for item in items:
                title = (item.get("snippet") or {}).get("title")
                print(f"CHANNEL: {item.get('id')} — {title}")
            print("Ready for headless uploads.")
    except Exception as exc:  # noqa: BLE001
        print(f"CHANNEL check failed: {exc}")
    print("=" * 40 + "\n")
    print("Keep youtube-token.json private (gitignored).")


if __name__ == "__main__":
    main()
