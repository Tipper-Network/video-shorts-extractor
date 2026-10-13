# Meta / Instagram setup checklist

Create a **Business** app. That is the only type that exposes `instagram_content_publish`. Do not pick Consumer or Gaming.

## 1. Create the app

1. [developers.facebook.com](https://developers.facebook.com/) → **My Apps** → **Create App**
2. What do you want your app to do? → **Other** → Next → **Business**
3. Name e.g. `G.A.F Automation`, contact email yours
4. Optional: link a Business Portfolio (or leave empty — Meta will create one)

## 2. Products + credentials

1. Left menu → **Add Products** → **Instagram** (Graph API) → Set Up  
   Facebook Login is usually added too — keep it.
2. **App Settings → Basic** → copy:
   - **App ID** → `META_APP_ID` / `APP_ID`
   - **App Secret** (Show) → `META_APP_SECRET` / `APP_SECRET`
3. Instagram Quickstart: connect the **Facebook Page** linked to your Instagram **Professional** account (e.g. `@guilds.adventurers.frontiers`).

## 3. Account requirements

- Instagram → **Professional** (Business or Creator)
- Facebook **Page** linked to that IG account  
  If Graph returns empty `instagram_business_account`: IG app → Settings → Account → Linked Accounts → Facebook Page.

## 4. Get `PAGE_ID` and `IG_BUSINESS_ID` (Graph Explorer)

1. Open [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Top right: select your app + a **Page** token for the Page linked to IG
3. Query:

```text
GET /me/accounts
```

Copy the Page `id` → `FACEBOOK_PAGE_ID` / `PAGE_ID`

4. Then:

```text
GET /{PAGE_ID}?fields=instagram_business_account
```

Response:

```json
{
  "instagram_business_account": { "id": "1784xxxxxxxxxxxx" }
}
```

That `id` → `IG_BUSINESS_ID` / `INSTAGRAM_BUSINESS_ACCOUNT_ID`

**Alternative (no API):** Meta Business Suite → Settings → Business Assets → Instagram Accounts → ID is in the URL: `.../instagram_accounts/{ID}/`

## 5. Long-lived token

1. Generate a User token with (eventually App Review for production):  
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, …
2. Exchange for a **long-lived** token (~60 days) → `META_ACCESS_TOKEN` / `ACCESS_TOKEN`
3. Refresh with `APP_ID` + `APP_SECRET` before expiry

## 6. Put values in `integrations/.env`

```bash
META_APP_ID=…
META_APP_SECRET=…
META_ACCESS_TOKEN=…          # long-lived
FACEBOOK_PAGE_ID=…           # from /me/accounts
IG_BUSINESS_ID=…             # from instagram_business_account.id
IG_SHARE_TO_FEED=false       # Reels tab only — not main grid (browser can't do this)
IG_COLLABORATORS=tipper.network,thehardport   # → collaborators=["tipper.network","thehardport"]
MEDIA_PUBLIC_BASE_URL=…      # public HTTPS base; Graph cannot read local disk
PUBLISH_DRY_RUN=true
```

## 7. Public video host (required)

Graph API **HTTP-fetches** `video_url`. Upload / sync mp4s to S3, Cloudinary, or any public HTTPS host, then set `MEDIA_PUBLIC_BASE_URL` (optional `MEDIA_PUBLIC_PREFIX`).

## 8. Feed vs Reels tab

- **Browser** Instagram: no “Also share to Feed” toggle — Reels always hit the grid.
- **Mobile app:** toggle exists on the Share screen.
- **Our agent:** `share_to_feed=false` on create-container (default). Snippets stay in the Reels tab; main grid stays for carousels / frameworks.

## Reference pack (first credential test)

Use this pack when verifying tokens + caption wiring — not a random catalog row:

```text
step-4-ready-to-post/founder/origin-story/03-trust/
  sh01_reaction-vs-response_story-first.md   ← ## Instagram **Caption:**
  sh01_reaction-vs-response_story-first.mp4
```

Agent reads the **Instagram** caption from the `.md` (not the YouTube description).

```bash
# Dry-run that exact pack (caption + paths; no Graph call if PUBLISH_DRY_RUN=true)
PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --example

# Live (needs IG_BUSINESS_ID + long-lived token + MEDIA_PUBLIC_BASE_URL with that mp4 hosted)
PUBLISH_DRY_RUN=false python3 content_pipeline/cli/publish/ig_publish_reels.py --example
```

## Dry run (catalog)

```bash
PUBLISH_DRY_RUN=true python3 content_pipeline/cli/publish/ig_publish_reels.py --limit 1
```
