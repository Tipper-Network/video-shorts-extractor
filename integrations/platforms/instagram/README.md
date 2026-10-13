# Instagram — Graph API Reels

**Agent stack:** Python (`content_pipeline/cli/publish/`).  
**Catalog:** Sheet / `step-4-ready-to-post/publish_catalog.csv`.  
**Gate:** only rows with `status=approved` (and optional `scheduled_date <= today`).  
**Setup:** [`docs/setup.md`](docs/setup.md) — create a **Business** app, then resolve `PAGE_ID` + `IG_BUSINESS_ID`.

Instagram Graph API **cannot read local disk**. Flow:

```text
step-4 .mp4 (local)
    → S3 upload → stable path-style URL
       https://s3.{region}.amazonaws.com/{bucket}/socials/{step-4 relative path}
       (bucket policy: public GetObject on socials/*; S3_USE_PRESIGN=true as fallback)
    → POST …/{IG_USER_ID}/media  (REELS + caption + share_to_feed=false)
    → poll creation_id status_code until FINISHED
    → POST …/media_publish
    → write instagram_url + status=posted on Sheet (when Sheets sync exists)
```

Local catalog column ``media_url`` stores the stable S3 URL after upload.

Smoke-test upload only:

```bash
python3 content_pipeline/cli/publish/s3_upload.py --example
```

## The two publish calls (per Reel)

```text
1) POST /v20.0/{IG_BUSINESS_ID}/media
     media_type=REELS
     video_url={PUBLIC_URL}
     caption={caption + hashtags}
     share_to_feed=false          ← Reels tab only (not main grid)
     collaborators=["tipper.network","thehardport"]   ← from IG_COLLABORATORS
     access_token={LONG_LIVED}

   → { "id": "<creation_id>" }

2) Poll GET /v20.0/{creation_id}?fields=status_code
     until status_code=FINISHED  (sleep ~10s; ERROR/EXPIRED → fail)

3) POST /v20.0/{IG_BUSINESS_ID}/media_publish
     creation_id={creation_id}
     access_token={LONG_LIVED}

   → { "id": "<media_id>" }
```

Between publishes: sleep **~60s** (throttling). Prefer **1/day** via catalog `scheduled_date` (e.g. 19:00 Asia/Beirut in the Sheet), not dumping 100 at once.

## Facebook Page Reels (different endpoint)

Optional (`PUBLISH_TO_FB`). Same public mp4 + Page token — **not** the IG `/media` path:

```text
POST /v20.0/{FACEBOOK_PAGE_ID}/video_reels
  file_url={PUBLIC_URL}
  description={caption}
  access_token={SAME_PAGE_TOKEN}
```

Code: `content_pipeline/lib/publish/facebook.py`

## Layout

```text
integrations/platforms/instagram/
├── README.md
├── docs/
│   └── setup.md              ← Business app + Graph Explorer IDs
├── credentials/              ← gitignored tokens (optional files)
└── (env lives in integrations/.env)

content_pipeline/
  lib/publish/
    instagram.py              ← Graph client (share_to_feed default false)
    media_host.py             ← public URL helper
  cli/publish/
    ig_publish_reels.py       ← loop from catalog
```

## Env (see `integrations/.env.example`)

| Variable | From |
|----------|------|
| `IG_BUSINESS_ID` / `INSTAGRAM_BUSINESS_ACCOUNT_ID` | `GET /{PAGE_ID}?fields=instagram_business_account` |
| `FACEBOOK_PAGE_ID` / `PAGE_ID` | `GET /me/accounts` (Page linked to IG Professional) |
| `META_ACCESS_TOKEN` / `ACCESS_TOKEN` | Long-lived, `instagram_content_publish` |
| `META_APP_ID` / `APP_ID` | App Settings → Basic (Business app) |
| `META_APP_SECRET` / `APP_SECRET` | Refresh token ~60 days |
| `IG_SHARE_TO_FEED` | Default `false` — Reels tab only |
| `IG_COLLABORATORS` | Comma usernames → JSON array on create (e.g. `tipper.network,thehardport`) |
| `MEDIA_PUBLIC_BASE_URL` or S3/Cloudinary | Host for mp4 before IG fetch |

Aliases accepted so either naming style works.

## Specs / gotchas

- MP4, 9:16, &lt; 1GB, ideally 3–90s (our shorts are ~50–75s)
- **Public `video_url` required** — upload first, then feed URL to Graph
- Poll until `FINISHED` before `media_publish`
- Browser upload cannot turn off feed share; API `share_to_feed=false` can
- App type must be **Business** or you will not get content publish permissions

## Reference pack + dry run

**Example for credential tests:**  
`step-4-ready-to-post/founder/origin-story/03-trust/sh01_reaction-vs-response_story-first.md`  
Caption comes from that file’s `## Instagram` → **Caption:** block.

```bash
# That pack only (recommended first run with credentials):
PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --example

PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --limit 1

# One due reel (scheduled_date <= today), still dry:
PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --due-only --limit 1
```
