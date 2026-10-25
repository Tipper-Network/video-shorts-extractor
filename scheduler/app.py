#!/usr/bin/env python3
"""Read-only schedule board. Sheet is the source of truth.

  python3 scheduler/app.py
  open http://127.0.0.1:8787
"""

from __future__ import annotations

import html
import json
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from due import is_due, today
from sheet_store import load_rows

HOST = "127.0.0.1"
PORT = 8787


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def _sort_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("scheduled_date") or "9999-99-99",
        row.get("entity") or "",
        row.get("publish_order") or "",
    )


def render(rows: list[dict[str, str]], source: str, error: str, day: date) -> bytes:
    due = [row for row in rows if is_due(row, now=day)]
    upcoming = [
        row
        for row in rows
        if (row.get("scheduled_date") or "") >= day.isoformat()
        and (row.get("status") or "").lower() != "posted"
    ]
    upcoming.sort(key=_sort_key)
    counts: dict[str, int] = {}
    for row in rows:
        status = (row.get("status") or "blank").lower()
        counts[status] = counts.get(status, 0) + 1

    def table(items: list[dict[str, str]]) -> str:
        body = []
        for row in items:
            title = row.get("youtube_title") or row.get("title") or ""
            href = row.get("youtube_url") or row.get("instagram_url") or ""
            title_html = (
                f'<a href="{_esc(href)}">{_esc(title)}</a>' if href else _esc(title)
            )
            status = (row.get("status") or "").lower()
            body.append(
                "<tr>"
                f"<td>{_esc(row.get('scheduled_date'))}</td>"
                f"<td>{_esc(row.get('entity'))}</td>"
                f"<td>{_esc(row.get('series'))}</td>"
                f"<td>{title_html}</td>"
                f'<td class="st st-{_esc(status)}">{_esc(status)}</td>'
                f"<td>{_esc(row.get('collaborators'))}</td>"
                "</tr>"
            )
        if not body:
            body.append('<tr><td colspan="6">None</td></tr>')
        return (
            "<table><thead><tr>"
            "<th>Date</th><th>Entity</th><th>Series</th><th>Title</th>"
            "<th>Status</th><th>Collabs</th>"
            "</tr></thead><tbody>"
            + "".join(body)
            + "</tbody></table>"
        )

    err = f'<p class="err">{_esc(error)}</p>' if error else ""
    chips = " ".join(
        f'<span class="chip">{_esc(name)} {_esc(n)}</span>'
        for name, n in sorted(counts.items())
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Schedule</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin: 0; font: 15px/1.45 ui-sans-serif, system-ui, sans-serif;
          background: #111; color: #eee; }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 28px 20px 64px; }}
  h1 {{ font-size: 28px; font-weight: 650; margin: 0 0 6px; }}
  h2 {{ font-size: 16px; margin: 28px 0 8px; letter-spacing: .02em; }}
  .meta {{ color: #9a9a9a; }}
  .err {{ color: #ffb4a8; }}
  .chip {{ display: inline-block; margin: 8px 8px 0 0; padding: 2px 8px;
           border: 1px solid #333; border-radius: 999px; color: #ccc; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #2a2a2a;
            vertical-align: top; }}
  th {{ color: #888; font-weight: 550; font-size: 12px; text-transform: uppercase; }}
  a {{ color: #d7c4a3; }}
  .st-scheduled {{ color: #f0d48a; }}
  .st-posted {{ color: #9dcaa8; }}
  .st-approved {{ color: #b9c7ef; }}
  .note {{ color: #888; max-width: 62ch; }}
</style>
</head>
<body>
<main>
  <h1>Schedule</h1>
  <p class="meta">Source: {_esc(source)} · Beirut today {_esc(day.isoformat())} · {len(rows)} rows</p>
  {err}
  <p>{chips}</p>
  <p class="note">Only rows marked <b>scheduled</b> in the Sheet are eligible for the clock.
  Approved stays parked until you change the status.</p>
  <h2>Due now ({len(due)})</h2>
  {table(due)}
  <h2>Still to post</h2>
  {table(upcoming[0:40])}
</main>
</body>
</html>
"""
    return page.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[schedule] {self.address_string()} {fmt % args}")

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in ("/", "/schedule"):
            rows, source, error = load_rows()
            self._send(200, render(rows, source, error, today()), "text/html; charset=utf-8")
            return
        if path == "/api/schedule":
            rows, source, error = load_rows()
            day = today()
            payload = {
                "source": source,
                "error": error,
                "today": day.isoformat(),
                "timezone": "Asia/Beirut",
                "due": [row for row in rows if is_due(row, now=day)],
                "counts": {},
            }
            counts: dict[str, int] = {}
            for row in rows:
                status = (row.get("status") or "blank").lower()
                counts[status] = counts.get(status, 0) + 1
            payload["counts"] = counts
            payload["rows"] = rows
            self._send(200, json.dumps(payload).encode(), "application/json")
            return
        if path == "/health":
            self._send(200, b'{"ok":true}\n', "application/json")
            return
        self._send(404, b"not found\n", "text/plain; charset=utf-8")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Schedule board http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
