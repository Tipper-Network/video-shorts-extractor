---
name: publish-schedule
description: How finished shorts get onto the live poster. Use when uploading to S3, editing the publish catalog, scheduling dates, or checking why cron-posting did or did not post.
---

# Publish schedule

Cutting stays on this machine. Posting runs on Dokploy in the nested repo `cron_posting/` (its own git repo; the parent `.gitignore` hides it). The website reads the schedule and hosts **Connect** for YouTube / Instagram. It does not post.

## Handoff

1. Mp4 is already at `s3://socials.bucket/socials/{path under step-4}`. The server does not upload from disk.
2. The Sheet tab `publish_catalog` has `youtube_title`, `description`, `hashtags`, `collaborators`, `scheduled_date` (`YYYY-MM-DD`), and `video_path`.
3. A human sets `status` to `scheduled`. `ready` and `approved` stay parked.

S3 key drops the `step-4-ready-to-post/` prefix. `video_path` in the Sheet is what the key is built from. Do not sort the header off row 1. Sort data rows by `scheduled_date`.

## When it posts

Asia/Beirut calendar day. A row is due when `status` is `scheduled` and `scheduled_date` is today or earlier. No time-of-day column. The API ticks every 15 minutes and posts **one** due row (oldest date, then `publish_order`) to Instagram and YouTube. `status` becomes `posted` only after both URLs are filled. A failed platform stays `scheduled` and is retried; the one that already has a URL is skipped.

Cadence as of 2026-10-25: **five posts a week, one per weekday** (Mon–Fri). Weekends empty.

YouTube always gets Sheet `youtube_title` (title) and `description` (details), plus `hashtags` as tags and in the description body, plus collaborator `@handles`. Do not upload a silent/untitled file.

## Credentials

Dokploy **API** environment only. Not in git. Not in the browser bundle. Not on the web service except `API_URL` / `NEXT_PUBLIC_API_URL`.

| Need | Variables |
|------|-----------|
| Sheet write | `GOOGLE_SHEETS_ID`, `GOOGLE_SHEETS_TAB=publish_catalog`, **`GOOGLE_SERVICE_ACCOUNT_JSON`** (preferred). Share the Sheet with the service-account email. |
| S3 read + token store | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION=eu-north-1`, `S3_BUCKET`, prefix `socials` |
| OAuth Connect | `OAUTH_GATE`, `PUBLIC_API_URL=https://api.cron-posting.psyferblock.io`, `PUBLIC_WEB_URL=https://cron-posting.psyferblock.io` |
| YouTube client | `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_CHANNEL_ID=UCKUS5W72IDOrWnhh-4wOxSw` — refresh token from Connect, stored in S3 |
| Instagram client | `META_APP_ID`, `META_APP_SECRET`, `IG_BUSINESS_ID`, `IG_COLLABORATORS=tipper.network,thehardport`, `IG_SHARE_TO_FEED=false` — long-lived token from Connect, stored in S3 |

Do not set `YOUTUBE_TOKEN_PATH` or `GOOGLE_OAUTH_TOKEN_PATH` on the server. `GOOGLE_CLIENT_ID` is not the name the API reads.

### Cloud Connect

1. YouTube OAuth client type **Web**. Redirect: `{PUBLIC_API_URL}/oauth/youtube/callback`. Consent screen **In production** (Testing kills refresh tokens in ~7 days).
2. Meta app Valid OAuth Redirect URIs: `{PUBLIC_API_URL}/oauth/instagram/callback`.
3. Board → Connect → paste `OAUTH_GATE` → Connect YouTube / Connect Instagram.
4. Tokens: `s3://…/socials/secrets/oauth-tokens.json`. Instagram auto-extends when under 14 days remain.
5. Check `GET /oauth/status` and `GET /health`.

Env `YOUTUBE_REFRESH_TOKEN` / `META_ACCESS_TOKEN` remain fallbacks until Connect writes S3.

Web service env: `API_URL` and `NEXT_PUBLIC_API_URL` = `https://api.cron-posting.psyferblock.io` (scheme required). Container ports: API `3001`, web `3000`.

## Docker note

API image must `rm -f tsconfig.tsbuildinfo` before `nest build` and `test -f dist/main.js`. Host incremental buildinfo makes Nest exit 0 with no `dist`.

## Already posted

Ten founder + GAF chunks are public on The G.A.F. channel. Do not schedule them again.

Four founder shorts (`origin-story` sh01, sh02, sh03, sh05) have no mp4 in step-4. They stayed `ready`.
