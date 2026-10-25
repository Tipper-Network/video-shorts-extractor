# USER.md — Editing Preferences & Active Projects

Stable directives for content creation sessions. One directive per entry.

## Directives

<!-- observed: 2026-09-02 | status: active -->

- Git ships the **product others onboard on** (`skills/`, `planning/`, `content_pipeline/`, templates). Job folders, brand books, and this file stay local. Cursor+folders now; website UI later — same agents, same shorts/chunks.

<!-- observed: 2026-09-02 | status: active -->

- When planning storyline or editorial tone, read the named entity's file in `brands/` first. Tipper, THP, and GAF are siblings; do not collapse them. Founder spoken style (`USER.md`, Origin Story cuts) applies to all three.

<!-- observed: 2026-09-02 | status: active -->

- Prefer chronological ordering for multi-clip projects unless the narrative explicitly calls for reordering.

<!-- observed: 2026-09-02 | status: active -->

- Skills sit in three organizations ([`skills/CATALOG.md`](skills/CATALOG.md)). Brand (`entity_brand`, `brands/`) before a cut. Selection (`situation_resolve`, `extract_shorts`, `chunks`) decides the lands. Edit subcategories run after the land is chosen. Posting strategies are later and do not choose the cut. The video name picks the entity (Tipper / THP / GAF). A short that states a situation and does not resolve it fails. A resolved short that belongs to a different entity is leftover, not a ship.

<!-- observed: 2026-09-02 | status: active -->

- Never delete planning, skills, or instinct files — they encode the editing approach. Edit and refine instead.

<!-- observed: 2026-09-02 | status: active -->

- Keep project-specific edit requirements in `content_pipeline/projects/{name}/requirements.md` — never mix into platform skills/code.

<!-- observed: 2026-09-02 | status: active -->

- When a project reveals a platform gap, fix the skill/script first, then log it in `planning/capability-matrix.md`.

<!-- observed: 2026-09-02 | status: active -->

- For multi-clip assembly: **draft concat first** (fast stream-copy), review timeline, then normalize only if needed for export.

<!-- observed: 2026-09-02 | status: active -->

- **Outcome:** 2 types of deliverables: **Shorts** (9:16, up to 3 editorial versions) and **Chunks** (16:9, 11-15 min). Never render YouTube / TikTok / Reels copies of the same cut.
- **Stage folders:** `step-1-projects/` → `step-2-viral-edit/` → `step-3-flywheel-organiser/` → `step-4-ready-to-post/` → `step-5-google-sheets/` (catalog/schedule). Dokploy posts only `scheduled` rows (`skills/publish_schedule/`). Queue: `step-1-projects/VIDEO-EDITS.md`.
- **Through folder 12 (2026-10-07):** batch viral→step-4 via `content_pipeline/cli/batch_to_step4.py`. After that run finishes → pause for new content + feedback. Program Future Ready stays paused until asked.
- **Viral end results:** under `{job}/viral/{shorts,covers,approved}/` in step-2. Cut masters stay in `output/deliverables/`. Never overwrite `output/` with captioned/typed finishes.
- **Caption height:** `margin_v` **500** on every captioned short (founder / tipper / gaf). Reburn with `content_pipeline/cli/reburn_caption_margin.py` — in place, no `_marginv*` copies. Post from `viral/approved/` or the step-4 pack only; stage1/stage2 are temp once approved is current.
- Story-first usually wins when the elaboration is kept; put the punchline hook on the front of that cut. Level speech on the finished file (`level_speech`: compressor + dynaudnorm + limiter + loudnorm −16 / LRA 4) so live spikes don't jump.
- Agent must not go silent on long ffmpeg/transcribe jobs — background them and keep responding.
- Never overwrite a rendered clip the user can already play. Next pass writes `_v2`, `_v3`, … so both files stay for A/B. Only `--force` replaces in place. Never land on an existing `_vN`.
- Script before picture. Write the playback script to `deliverables/shorts/{stem}.md` (theme, problem, context, resolve + transcript lines). Wait for approval. Do not ffmpeg until the script is signed off. Draft mp4s stay in `shorts/`. Approved videos go to `deliverables/shorts_approved/`.
- Shorts duration: **50s floor, ~60s+ is the average.** Do not ship a speech short under 50s. Prefer 55–75s. Hard ceiling still 90s. Complete resolve still wins, but pad by holding the situation (more of the same thought), not by splicing a second story.
- Do not out mid-clause to dodge a pitch. If the land is “right now,” keep the finished example of the move.
- Any plan takes as many shorts as the tape can hold. After the named themes are scripted, scan the leftover transcript and keep every other land that resolves. The brief is not a cap. A finished stage set is not a reason to stop.
- Full-file script: YouTube `.srt` when the upload is the same file as `input/`. Whisper the locked window only, not the whole lecture.
- GAF Future Ready lectures: titled plains in `output/transcript/` (`13. Future Ready, The Program.txt`, …) are the ebook source. Clocked copies stay in each lecture folder.
- GAF prints as **Guilds, Adventurers, and Frontiers** (guild of guilds). Not “Guild of Adventurers and Frontiers.”
- Future Ready voice locks: stretch = day he moved to the ocean / chose to buy the island not live as a bum (story is in GAF 9–12, not in this job yet). Restaurant chosen because financially liquid. Girlfriend = stacked ships (friendship + partnership + commitment), not a swapped work example. Cosmetic friend stays, anonymous. Lecture 16 cold open is not a hole. Ships = you go out of yourself and come back. Agents = feedback loop, mutual support, better instructions. The six lectures *are* the designed month. Two yous: whatever is internal reflects external — do not invent a me/self/I diagram he did not draw.
- AI Influencer Cheat Sheet skills live in `~/.cursor/skills/` (`charsheet-soul`, `ugc-influencer-video`, `content-engine`, `digital-product`). Do not copy them into repo `skills/` — that tree is the cut engine. Source zips stay in `AI Influencer Cheat Sheet/skills/`.
- **YouTube handles (collabs):** Tipper `@tippernetwork`, Hard Port `@Thehardport0`. Catalog/Sheet column `collaborators` (comma handles, no `@`). Defaults: GAF/founder → `tippernetwork,Thehardport0`; Tipper → `Thehardport0`. YouTube API has no collab invite — credit in description/tags; true collab badge = Studio. IG usernames stay in `IG_COLLABORATORS` (`tipper.network,thehardport`).

<!-- observed: 2026-10-25 | status: active -->

- **Posting is Dokploy, not this laptop.** Skill: `skills/publish_schedule/`. Sheet `publish_catalog` is the queue. Only `status=scheduled` and `scheduled_date` ≤ today (Asia/Beirut) is due. Cadence: **one post each weekday** (five a week). Sort the Sheet by `scheduled_date`; never sort the header off row 1. `ready` / `approved` do not post.
- Secrets live in the Dokploy **API** env (`YOUTUBE_*`, `GOOGLE_OAUTH_*`, `META_ACCESS_TOKEN`, AWS). Do not commit them. Do not put token file paths on the server. The web app only gets `API_URL=https://api.cron-posting.psyferblock.io`.
- YouTube: one browser sign-in after the OAuth app is published. The refresh token posts forever; the one-hour access token renews itself. Instagram tokens die after ~60 days and must be replaced by hand. The current IG token expired 2026-10-13.

## Active Projects

<!-- observed: 2026-09-02 | status: active -->

- **Tipper The Social Structures** (`projects/5. tipper the social structures/`) — Entity Tipper. Shorts + chunks extracted. Gemini `shorts.md` contrast only. Source filename keeps typo `Stuctures`.
- **Tipper The Startup** (`projects/4. tipper the startup/`) — Entity Tipper. Shorts + chunks extracted. Scripts in `shorts_extraction.md` / `chunk_extraction.md`. Gemini `shorts.md` contrast only. No sidecar `.srt`.
- **Tipper The Concept** — extracted 2026-09-21. Folder now under `~/Desktop/ready to post/3. tipper the concept/`.
- **Tipper The Start of the Project** (`projects/6. tipper the start of the project/`) — extracted. 9 shorts + 3 chunks. Do not re-transcribe.
- **Tipper The Work** (`projects/7. tipper the work/`) — extracted. 9 shorts + 3 chunks. Publish sh03→sh04→sh06→sh05→sh07→sh08→sh09→sh01→sh02. Do not re-transcribe.
- **Tipper The Effort** (`projects/8. tipper the effort/`) — extracted. 9 shorts + 3 chunks. Publish sh03→sh01→sh02→sh05→sh06→sh07→sh09→sh08→sh04. Do not re-transcribe.
- **Tipper The Change** (`projects/9. tipper the change/`) — extracted. 9 shorts + 3 chunks. Publish sh08→sh09→sh04→sh03→sh05→sh06→sh02→sh01→sh07. Do not re-transcribe.
- **GAF Qualifications 1–3** (`10 qualifications 1`–`12 qualifications 3`) — extracted. Entity GAF. Plan from SRT. Do not Whisper. Do not close on Tipper. Pt 3 is 2 chunks (THP supercut skip; third under floor).
- **Tipper The Origin Story** (`projects/2. tipper the origin story/`) — Entity Tipper. Shorts + chunks extracted. Scripts in `shorts_extraction.md` / `chunk_extraction.md`. Not founder Origin Story (`0.`).
- **The-GAF-program Future Ready** (`step-1-projects/The-GAF-program future ready vids/`) — GAF. October 7 renders are trashed. Reselect is stage-first (2026-10-25): several shorts may share a stage, a missing stage is skipped, service is the chunk. Lecture 13 holds five of six stages (no referral). Do not ffmpeg until that slate is signed. Do not Whisper.
- **Tipper The Story** (`projects/1. tipper the story/`) — Shorts: `shorts_extraction.md`. Chunks rendered: `ch01_common-ground.mp4`, `ch02_show-you-their-world.mp4`. Gemini unused.
- **Origin Story** — Approved: sh01 story-first (100s), sh02 island-bum hook-first (64s), sh03 focus-vs-tunnel hook-first (58s), sh05 moving-house first-stream close (44s). Draft: sh04 Game WITH Life (28s). Chunks: ch01, ch02. Deferred: ch03.
