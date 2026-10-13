"""Facebook Page Reels — POST /{FACEBOOK_PAGE_ID}/video_reels.

Different from Instagram Graph Reels:
  IG  →  /{IG_BUSINESS_ID}/media  +  /media_publish
  FB  →  /{FACEBOOK_PAGE_ID}/video_reels  (file_url + description)
"""

from __future__ import annotations

from typing import Any

import requests

from publish.env import first

GRAPH = "https://graph.facebook.com/v20.0"


class FacebookConfigError(RuntimeError):
    pass


def config() -> dict[str, str]:
    page_id = first("FACEBOOK_PAGE_ID", "PAGE_ID")
    token = first("META_ACCESS_TOKEN", "ACCESS_TOKEN")
    if not page_id or not token:
        raise FacebookConfigError(
            "Need FACEBOOK_PAGE_ID and META_ACCESS_TOKEN (EAA…) in integrations/.env"
        )
    if not token.startswith("EAA"):
        raise FacebookConfigError(
            "META_ACCESS_TOKEN must be a Graph token starting with EAA"
        )
    return {"page_id": page_id, "token": token}


def publish_page_reel(
    *,
    file_url: str,
    description: str,
    page_id: str | None = None,
    token: str | None = None,
) -> dict[str, Any]:
    """POST /{page_id}/video_reels — returns Graph JSON (includes id when ok)."""
    cfg = config()
    page_id = page_id or cfg["page_id"]
    token = token or cfg["token"]
    r = requests.post(
        f"{GRAPH}/{page_id}/video_reels",
        data={
            "file_url": file_url,
            "description": description,
            "access_token": token,
        },
        timeout=180,
    )
    data = r.json()
    if r.status_code >= 400 or data.get("error"):
        raise RuntimeError(f"FB video_reels failed: {data}")
    return data
