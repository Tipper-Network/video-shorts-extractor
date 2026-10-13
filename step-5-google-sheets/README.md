# Step 5 — Google Sheets (publish catalog)

Jobs land here **conceptually** after step-4 packs exist. This folder holds Sheet sync config + credentials — not the video files (those stay in step-4).

**Sheet = titles, schedule, status.** Platforms (step-6 later) upload from `video_path` on approved rows.

## Layout

```text
step-5-google-sheets/
├── README.md
├── PLAN.md                 ← automation roadmap (YT / IG / TikTok)
├── config.example.env
├── credentials/            ← gitignored secrets
│   ├── oauth-client.json
│   ├── token.json
│   └── service-account.json
└── sync/                   ← push/pull scripts (next)
```

Catalog on disk (source): [`../step-4-ready-to-post/publish_catalog.csv`](../step-4-ready-to-post/publish_catalog.csv)

Live Sheet ID (in workspace `.env`):

```bash
GOOGLE_SHEETS_ID=1kxKUbKUETiRT-bf69AcAMOERAbNdRsf9yobZrNWuyvw
GOOGLE_SHEETS_CREDENTIALS=step-5-google-sheets/credentials/oauth-client.json
```

## What this step does

1. Import / push `publish_catalog.csv` → your Google Sheet.  
2. You edit schedule, titles, `status` in Sheets.  
3. Later: sync scripts keep Sheet ↔ local catalog aligned.  
4. When `status=approved`, a **platform** adapter (not this folder) uploads the file.

## Setup checklist

- [ ] Sheet created + CSV imported  
- [ ] `GOOGLE_SHEETS_ID` in `.env` (the `/d/<id>/` part of the URL)  
- [ ] Sheets API enabled in Google Cloud  
- [ ] `credentials/oauth-client.json` (Desktop OAuth) **or** service-account JSON shared on the Sheet  
- [ ] First sync → writes `credentials/token.json` (OAuth only)

Details: [`config.example.env`](config.example.env). Platform plan: [`PLAN.md`](PLAN.md).
