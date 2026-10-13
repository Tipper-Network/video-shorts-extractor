# Next: automation without Postiz

Step-5 owns the **Sheet**. Uploading is a following stage (call it step-6 when we add the folder).

```text
step-4 pack (mp4 + .md)
    → step-5 Sheet row (title, caption, scheduled_date, video_path, status)
    → platform upload when status=approved
    → Sheet: posted_at + youtube_url / instagram_url / tiktok_url
```

## Cadence (already in catalog)

| Pillar | Day |
|--------|-----|
| fascinate | Monday |
| educate | Wednesday |
| invite | Thursday |
| social_proof | Saturday (every other Sat open for personalised) |

## Platform order (DIY APIs)

| Order | Platform | Why |
|------:|----------|-----|
| 1 | **YouTube** | Same Google Cloud as Sheets. Data API upload Shorts. Fastest to ship. |
| 2 | **Instagram** | Meta Graph Reels. Needs IG Professional + Facebook Page + app (often review). |
| 3 | **TikTok** | Content Posting API. Developer app + posting approval — slowest gate. |

No Postiz SaaS. Credentials under `integrations/platforms/{youtube,instagram,tiktok}/credentials/`.

## Status machine (Sheet column)

`ready` → `approved` → `scheduled` → `posted` (or `error`)

Nothing public until `approved` (`SOUL.md`).

## Discussion points (decide with operator)

1. **One Sheet tab vs tab-per-entity** — Tipper / GAF / founder filters or separate tabs?  
2. **YouTube first only?** — Ship YT Shorts automation while IG/TT keys are pending.  
3. **Channels** — one Google/YouTube login vs separate Tipper / GAF / founder channels.  
4. **Who clicks approve?** — you in the Sheet, or agent asks once per day batch.  
5. **Personalised Saturdays** — manual rows only, or a second “personal” series later.

## Immediate next engineering (when you say go)

1. `sync/push_catalog.py` — CSV → Sheet (create/update rows by `entity+series+id`).  
2. YouTube OAuth + `upload_short.py` reading approved rows for today’s date.  
3. **Instagram skeleton done** — `cli/publish/ig_publish_reels.py` (needs Meta env + public media URL).  
4. TikTok adapter when app exists.
