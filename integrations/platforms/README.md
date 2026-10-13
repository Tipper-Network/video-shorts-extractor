# Platforms — YouTube / Instagram / TikTok (no Postiz)

Postiz cloud is skipped (paid). Options to reach the same three networks:

## Instagram (structured)

See [`instagram/README.md`](instagram/README.md) + Python:

- `content_pipeline/lib/publish/instagram.py` — container → poll → publish  
- `content_pipeline/cli/publish/ig_publish_reels.py` — catalog loop  

Agent stack = **Python** (this repo). Schedule from Sheet/catalog (`--due-only`, 1/day), not a blind 100 dump. Default `share_to_feed=false` (Reels tab only). App type must be **Business** — see [`instagram/docs/setup.md`](instagram/docs/setup.md).

## Option A — Official APIs (DIY, free quotas)

| Platform | API | Realistic for us | Needs from you |
|----------|-----|------------------|----------------|
| **YouTube** | [YouTube Data API v3](https://developers.google.com/youtube/v3) resumable upload | **Best first.** Shorts = vertical upload + `#Shorts` / Shorts UI. | Google Cloud project (can share with Sheets), OAuth, YouTube channel |
| **Instagram** | Meta Graph API — Reels publishing | Medium. Instagram **Professional** account linked to a Facebook Page + Meta app. Production often needs App Review. | Meta Developer app, Page + IG Business/Creator, tokens |
| **TikTok** | [Content Posting API](https://developers.tiktok.com/) | Hardest. App + often **audit/approval** before open posting. | TikTok developer app, approved scopes |

Sync model stays the same as planned with Postiz:

```text
Sheet row (title, caption, scheduled_date, video_path, status=approved)
    → our script uploads that local mp4 + copy via each API
    → Sheet gets URLs + status=posted
```

**Suggested order:** YouTube first → Instagram → TikTok (as access unlocks).

Credentials live under:

```text
integrations/platforms/
  youtube/credentials/     # gitignored
  instagram/credentials/
  tiktok/credentials/
```

## Option B — Self-host an open scheduler (still free)

Self-host [Postiz](https://github.com/gitroomhq/postiz-app) or similar on your own machine/VPS. No SaaS fee; you pay only for the server. Same Sheet → draft → approve flow. Heavier ops than Option A.

## Option C — Sheet-only + manual upload (zero API)

Catalog already has dates and paths. You post by hand on schedule; we mark `posted` in the Sheet. No platform keys. Fine until APIs are ready.

## Recommendation

1. Finish **Google Sheets** sync (catalog online).  
2. Connect **YouTube** via official API (same Google Cloud project as Sheets).  
3. Add IG / TikTok when Meta + TikTok apps are approved — same Sheet columns, different upload adapters.

We do **not** auto-post until `status=approved` (see `SOUL.md`).
