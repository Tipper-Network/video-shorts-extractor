# Publish stack — next steps

Status as of **2026-10-13**: first live GAF Reel via Graph succeeded  
(`ig-test` → https://www.instagram.com/reel/DecfFDRCb6i/).  
IG has **no** native schedule field — we own the clock.

---

## What we already have

| Piece | Location |
|-------|----------|
| Env / tokens | `integrations/.env` |
| IG create → poll → publish | `content_pipeline/lib/publish/instagram.py` |
| Catalog-driven CLI | `content_pipeline/cli/publish/ig_publish_reels.py` |
| S3 upload + stable public URL | `content_pipeline/lib/publish/media_host.py` |
| Local catalog | `step-4-ready-to-post/publish_catalog.csv` |
| Cadence pillars | Mon fascinate / Wed educate / Thu invite / Sat social_proof (alt Sat open) |
| Flywheel order | step-3 `publish_order` + `flywheel_stage` |

**Schedule model (locked):** Sheet/catalog holds `scheduled_date` + `scheduled_time` + timezone.  
At that moment, **our code** runs create-container → wait `FINISHED` → `media_publish`.  
Do not use `--ignore-schedule` except conscious “post now.”

---

## Decision: who runs the clock?

### Recommended path (simple → grow)

**Phase 1 — cron on this machine (or a cheap VPS)**  
- One cron (or systemd timer) in **Asia/Beirut**.  
- e.g. every 15 min: `ig_publish_reels.py --due-only --limit 1` (and later YT/TT).  
- “Due” = `status=scheduled` and `scheduled_date`+`scheduled_time` ≤ now.  
- No always-on server required yet. Machine must be on (or use a $5 VPS).

**Phase 2 — small always-on worker (when cron on laptop is annoying)**  
- Tiny VPS / Fly / Railway / a home NUC.  
- Same Python CLI, or a thin loop that wakes every N minutes.  
- Secrets via env file or host secrets — never commit `.env`.

**Phase 3 — optional DB + API (only if Sheet friction is real)**  
- Postgres (e.g. Neon) mirrors Sheet rows: status, paths, media_url, due_at.  
- Worker: `SELECT … WHERE status='scheduled' AND due_at <= now()` → publish → write URLs.  
- Sheet remains the **human** UI; DB is the **runtime** queue. Sync Sheet ↔ DB on approve/schedule.

**Not recommended yet:** Node `node-cron` rewrite. Keep Python — we already have the Graph + S3 path.

**Facebook Page** posts *can* use Meta `scheduled_publish_time`; that’s a separate adapter (`PUBLISH_TO_FB`). IG stays “our cron.”

---

## Checklist — finish setup

### A. Google Sheets (step-5)

- [ ] Sheets API enabled; OAuth **or** service account JSON in `step-5-google-sheets/credentials/`
- [ ] Sheet shared with that identity; `GOOGLE_SHEETS_ID` set
- [ ] Sync scripts: push/pull `publish_catalog.csv` ↔ Sheet
- [ ] Columns aligned: entity, series, id, flywheel_stage, publish_order, content_pillar, scheduled_date, scheduled_time, timezone, status, video_path, media_url, captions/titles, posted_at, instagram_url, youtube_url, tiktok_url
- [ ] Filter views: by week / by entity / remaining (`status ≠ posted`)

### B. Scheduling discipline

- [ ] Default post time per entity (e.g. GAF `19:00` or `02:00` Asia/Beirut) — pick one and stick
- [ ] Rolling horizon 6–8 weeks of pillar slots
- [ ] Flex slots for tests / drops (don’t steal flywheel spine)
- [ ] Status gate: `ready` → `approved` → `scheduled` → `posted`
- [ ] CLI: due = date+time (extend beyond date-only `--due-only`)
- [ ] Cron or systemd timer documented in this folder

### C. Content path (don’t skip viral)

- [ ] Shorts get stage1 captions (`margin_v` 500) + stage2 sounds before step-4
- [ ] Pack `.md` has full YT / IG / TT copy before `scheduled`
- [ ] S3 `media_url` stable + public `GetObject` on `socials/*`
- [ ] After post: catalog URLs + move pack → `step-6-posted/`

### D. Meta / IG hygiene

- [ ] Long-lived token with `instagram_content_publish` + `instagram_basic`; refresh ~60 days
- [ ] `IG_BUSINESS_ID` = Page’s `instagram_business_account.id` (not Page id)
- [ ] Token app matches the Business app in use
- [ ] Collaborators / `share_to_feed` policy per entity documented

### E. Later platforms

- [ ] YouTube Shorts upload from same catalog rows
- [ ] TikTok when app approved
- [ ] Optional FB Page scheduled posts (true Meta schedule)

### F. Optional always-on

- [ ] VPS + cron, **or**
- [ ] Neon (or similar) queue table + worker polling due rows
- [ ] Health ping / failure alert (email or Telegram) on publish ERROR

---

## Near-term engineering order

1. Sheet sync (push/pull) + `scheduled_time` respected in `--due-only`.  
2. Beirut cron entry (15 min) calling IG publisher `--due-only --limit 1`.  
3. Document token refresh + PAB/S3 public-read reminder.  
4. Assign-next-slot helper (pillar day + empty horizon cell).  
5. Only then: VPS / DB if local cron is unreliable.

---

## Operator reminder

- **Success path proven:** S3 → Graph create → poll → publish → permalink.  
- **Schedule path:** catalog/Sheet datetime → **our** job fires publish.  
- **Editing path:** captions/sounds before “ready to post,” not folder-copy only.
