---
name: publish-schedule
description: How finished shorts get onto the live poster. Use when uploading to S3, editing the publish catalog, scheduling dates, or checking why cron-posting did or did not post.
---

# Publish schedule

Cutting stays on this machine. Posting runs on Dokploy in the nested repo `cron_posting/` (its own git repo; the parent `.gitignore` hides it). The website only reads the schedule. It does not sign in and it does not post.

## Handoff

1. Mp4 is already at `s3://socials.bucket/socials/{path under step-4}`. The server does not upload from disk.
2. The Sheet tab `publish_catalog` has `youtube_title`, `description`, `hashtags`, `collaborators`, `scheduled_date` (`YYYY-MM-DD`), and `video_path`.
3. A human sets `status` to `scheduled`. `ready` and `approved` stay parked.

S3 key drops the `step-4-ready-to-post/` prefix. `video_path` in the Sheet is what the key is built from. Do not sort the header off row 1. Sort data rows by `scheduled_date`.

## When it posts

Asia/Beirut calendar day. A row is due when `status` is `scheduled` and `scheduled_date` is today or earlier. No time-of-day column. The API ticks every 15 minutes and posts **one** due row (oldest date, then `publish_order`) to Instagram and YouTube. `status` becomes `posted` only after both URLs are filled. A failed platform stays `scheduled` and is retried; the one that already has a URL is skipped.

Cadence as of 2026-10-25: **five posts a week, one per weekday** (Mon–Fri). Weekends empty. 99 scheduled rows run 2026-10-26 through 2027-03-11.

## Credentials

Dokploy **API** environment only. Not in git. Not in the browser. Not on the web service.

| Need | Variables |
|------|-----------|
| Sheet write | `GOOGLE_SHEETS_ID`, `GOOGLE_SHEETS_TAB=publish_catalog`, `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN` |
| S3 read | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION=eu-north-1`, `S3_BUCKET` or `S3_BUCKET_NAME`, prefix defaults to `socials` |
| YouTube | `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, `YOUTUBE_CHANNEL_ID=UCKUS5W72IDOrWnhh-4wOxSw` |
| Instagram | `META_ACCESS_TOKEN`, `IG_BUSINESS_ID`, `IG_COLLABORATORS=tipper.network,thehardport`, `IG_SHARE_TO_FEED=false` |

Do not set `YOUTUBE_TOKEN_PATH` or `GOOGLE_OAUTH_TOKEN_PATH` on the server. Those paths exist only on this laptop. `GOOGLE_CLIENT_ID` is not the name the API reads.

YouTube access tokens last one hour. The refresh token is what stays on the server; the library renews the hour by itself. A Cloud OAuth app left in **Testing** kills that refresh token after 7 days. Publish the consent screen, sign in once, and do not run the login script again.

Instagram user tokens last about 60 days and do not refresh themselves. The token in env expired **2026-10-13**. It was also issued by a different Meta app than `META_APP_ID`. Replace it before an Instagram post can succeed.

Web service env: `API_URL` and `NEXT_PUBLIC_API_URL` = `https://api.cron-posting.psyferblock.io` (scheme required). Container ports: API `3001`, web `3000`.

## Already posted

Ten founder + GAF chunks are public on The G.A.F. channel (see `integrations/platforms/youtube/credentials/chunk_upload_log.json`). Do not schedule them again. `yt_publish_videos.py` is a placeholder, not that uploader.

Four founder shorts (`origin-story` sh01, sh02, sh03, sh05) have no mp4 in step-4. They stayed `ready`.
