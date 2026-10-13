# Publish catalog

**File:** [`publish_catalog.csv`](publish_catalog.csv) — 112 rows (jobs 0–12).

## Cadence (content pillars)

| Pillar | Weekday | Flywheel stages mapped |
|--------|---------|------------------------|
| **fascinate** | Monday | `attract`, `trust` |
| **educate** | Wednesday | `service` |
| **invite** | Thursday | `engage`, `loop` |
| **social_proof** | Saturday | `referral` — **every other Sat only** (open Sats for personalised proof) |

Schedule starts **Monday 2026-10-12**. Dates are per **entity** (Tipper / GAF / founder can post the same weekday on different accounts).

`status` starts as `ready`. Later: `drafted` → `approved` → `scheduled` → `posted`.

## Import to Google Sheets

1. Create a blank Sheet.
2. File → Import → Upload `publish_catalog.csv` → Replace current sheet.
3. Freeze row 1. Optional: Data → Filter views by `entity` / `status`.

## What we need from you to connect automation

### Google Sheets (catalog sync)

Pick one:

**A — Service account (best for agent scripts)**  
1. Google Cloud project → enable **Google Sheets API** (+ Drive API if uploading CSV).  
2. Create a **service account** → download JSON key.  
3. Put key at e.g. `~/.config/content-pipeline/google-sheets.json` (gitignored).  
4. Share your Sheet with the service account email (`…@….iam.gserviceaccount.com`) as **Editor**.  
5. Send me the **Sheet ID** (from the URL: `docs.google.com/spreadsheets/d/<SHEET_ID>/edit`).

**B — OAuth (you sign in once)**  
Same APIs enabled; I walk you through a one-time browser login; token stored locally (gitignored).

### Platforms (schedule → post)

Still need a publisher (e.g. **Postiz**):

1. Postiz account + API/MCP key  
2. Connected channels: YouTube / Instagram / TikTok per entity (Tipper, GAF, founder)  
3. Confirm: drafts only until you approve (default)

Sheet holds schedule + status. Postiz (or equivalent) uploads on `scheduled_date` after `approved`.
