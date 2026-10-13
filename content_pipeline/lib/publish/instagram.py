"""Instagram Graph API — create Reel container → poll → publish.

Default: share_to_feed=false so Reels land in the Reels tab only
(not the main profile grid). Browser upload cannot do that; API can.

Collaborators (optional): IG_COLLABORATORS=tipper.network,thehardport
sent as JSON array ["tipper.network","thehardport"] on create-container.
"""

from __future__ import annotations

import json
import time
from typing import Any

import requests

from publish.env import first

GRAPH = "https://graph.facebook.com/v20.0"


class InstagramConfigError(RuntimeError):
    pass


def _share_to_feed() -> bool:
    """Default false — snippets stay off the main grid."""
    return first("IG_SHARE_TO_FEED", default="false").lower() in (
        "1",
        "true",
        "yes",
    )


def list_collaborators() -> list[str]:
    """Usernames from ``IG_COLLABORATORS`` (comma-separated, no @)."""
    raw = first("IG_COLLABORATORS", default="")
    if not raw:
        return []
    out: list[str] = []
    for part in raw.split(","):
        u = part.strip().lstrip("@")
        if u:
            out.append(u)
    return out


def config() -> dict[str, str]:
    ig_id = first("IG_BUSINESS_ID", "INSTAGRAM_BUSINESS_ACCOUNT_ID")
    token = first("META_ACCESS_TOKEN", "ACCESS_TOKEN", "IG_ACCESS_TOKEN")
    page_id = first("FACEBOOK_PAGE_ID", "PAGE_ID")
    app_id = first("META_APP_ID", "APP_ID")
    app_secret = first("META_APP_SECRET", "APP_SECRET")
    if not ig_id or not token:
        raise InstagramConfigError(
            "Need IG_BUSINESS_ID (or INSTAGRAM_BUSINESS_ACCOUNT_ID) "
            "and META_ACCESS_TOKEN (or ACCESS_TOKEN) in integrations/.env — "
            "see integrations/platforms/instagram/docs/setup.md"
        )
    if not token.startswith("EAA"):
        raise InstagramConfigError(
            "META_ACCESS_TOKEN must be a long-lived Graph token starting with EAA "
            "(Graph Explorer → Generate Token → exchange for long-lived)"
        )
    return {
        "ig_id": ig_id,
        "token": token,
        "page_id": page_id,
        "app_id": app_id,
        "app_secret": app_secret,
    }


def create_reel_container(
    *,
    video_url: str,
    caption: str,
    ig_id: str | None = None,
    token: str | None = None,
    share_to_feed: bool | None = None,
    collaborators: list[str] | None = None,
) -> str:
    """POST /{IG_BUSINESS_ID}/media — returns creation_id.

    Shape::

        media_type=REELS
        video_url=…
        caption=…
        share_to_feed=false
        collaborators=["tipper.network","thehardport"]   # optional
        access_token=…
    """
    cfg = config()
    ig_id = ig_id or cfg["ig_id"]
    token = token or cfg["token"]
    if share_to_feed is None:
        share_to_feed = _share_to_feed()
    if collaborators is None:
        collaborators = list_collaborators()

    payload: dict[str, Any] = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true" if share_to_feed else "false",
        "access_token": token,
    }
    if collaborators:
        # Graph expects a JSON array of Instagram usernames (no @)
        payload["collaborators"] = json.dumps(collaborators)

    r = requests.post(
        f"{GRAPH}/{ig_id}/media",
        data=payload,
        timeout=120,
    )
    data = r.json()
    if "id" not in data:
        raise RuntimeError(f"create container failed: {data}")
    return str(data["id"])

def wait_until_finished(
    creation_id: str,
    *,
    token: str | None = None,
    poll_seconds: int = 10,
    timeout_seconds: int = 600,
) -> dict[str, Any]:
    cfg = config()
    token = token or cfg["token"]
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        r = requests.get(
            f"{GRAPH}/{creation_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=60,
        )
        data = r.json()
        status = data.get("status_code")
        if status == "FINISHED":
            return data
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {creation_id} failed: {data}")
        time.sleep(poll_seconds)
    raise TimeoutError(f"container {creation_id} not FINISHED within {timeout_seconds}s")


def publish_reel(
    creation_id: str,
    *,
    ig_id: str | None = None,
    token: str | None = None,
) -> str:
    cfg = config()
    ig_id = ig_id or cfg["ig_id"]
    token = token or cfg["token"]
    r = requests.post(
        f"{GRAPH}/{ig_id}/media_publish",
        data={"creation_id": creation_id, "access_token": token},
        timeout=120,
    )
    data = r.json()
    if "id" not in data:
        raise RuntimeError(f"publish failed: {data}")
    return str(data["id"])


def publish_reel_from_url(
    *,
    video_url: str,
    caption: str,
    throttle_seconds: int = 60,
    share_to_feed: bool | None = None,
    collaborators: list[str] | None = None,
) -> str:
    """Full create → poll FINISHED → publish. Returns published media id."""
    creation_id = create_reel_container(
        video_url=video_url,
        caption=caption,
        share_to_feed=share_to_feed,
        collaborators=collaborators,
    )
    wait_until_finished(creation_id)
    media_id = publish_reel(creation_id)
    if throttle_seconds > 0:
        time.sleep(throttle_seconds)
    return media_id
