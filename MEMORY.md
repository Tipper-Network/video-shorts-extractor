# MEMORY.md — Pipeline Decisions

Durable facts and decisions for the content pipeline workspace. Not user preferences (those go in `USER.md`).

## Workspace Scope (2026-09-02)

This workspace is the **local video editing and content creation pipeline** — separate from:

- **THP** (`~/Desktop/The-Hard-Port-stuff/The Hard Port/the-hard-port-os/`) — brand strategy, series scripts, editorial voice
- **Tipper** and other product repos — application code

THP defines *what* to say **when the video is a THP video**. Tipper and GAF have their own brand records. The title picks which one. This workspace still only executes the cut.

| Entity | Brand file in this repo |
|--------|-------------------------|
| Tipper | [`brands/Tipper_Brand_Book.md`](brands/Tipper_Brand_Book.md) |
| THP | [`brands/the-hard-port-brief.md`](brands/the-hard-port-brief.md) |
| GAF | [`brands/GAF_Brand_Brief.md`](brands/GAF_Brand_Brief.md) + [`brands/GAF_Brand_Book_Updated.md`](brands/GAF_Brand_Book_Updated.md) |
| founder | Spoken style only (`USER.md` + Origin Story cuts) |

## Architecture Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-09-01 | Plan → review → render (not one-shot) | Human QA cheaper than bad ffmpeg burns |
| 2026-09-01 | Map-reduce for chapters | 2hr transcript exceeds LLM context |
| 2026-09-01 | Separate plan + render scripts | Clear handoff, reusable transcripts |
| 2026-09-01 | Series JSON for flywheel | Continuity across episodes |
| 2026-09-02 | Keep planning/skills/instincts intact | They encode the editing approach — edit, don't delete |
| 2026-09-02 | THP strategy stays external | Avoid duplicating content docs; link and execute here |
| 2026-09-02 | Cursor agent is the planner; Ollama removed | Agent plans in-session from transcript + instincts; no local LLM server |
| 2026-09-12 | Re-renders write `_vN` compare copies | Need the previous file on disk to A/B audio/cut changes |
| 2026-09-12 | Script `.md` before any ffmpeg | Theme / problem / context / resolve get checked on paper. Drafts in `shorts/`, signed-off in `shorts_approved/` |
| 2026-09-21 | Title = entity brand key | Tipper / THP / GAF are siblings. Founder style is how he talks; entity is which queue the cut is for. |
| 2026-09-21 | Git = onboardable product | Clone ships skills, scripts, playbooks, `_template`s. Jobs, brand books, USER/MEMORY stay local. Website UI later; same agents, same manifest. |
| 2026-09-21 | YouTube `.srt` first, Whisper on the cut | Same-file YouTube captions recover more words than Whisper `small`. Plan from linearized SRT. Whisper only the locked 50–90s window to tighten clocks / GAF / uncensored speech. |
| 2026-09-21 | Faster render: copy concat, no 16:9 upscale, parallel shorts | Supercut `-c copy` (fallback re-encode). Chunks stay source size, cap 1920. Shorts `--jobs 4`. Sidecar `.srt` skips full-file Whisper. |
| 2026-09-23 | Cheat-sheet influencer skills stay personal | `charsheet-soul`, `ugc-influencer-video`, `content-engine`, `digital-product` install to `~/.cursor/skills/`. Repo `skills/` stays the cut engine. |
| 2026-09-23 | Viral finish ≠ `output/` | Step-2 writes captions/type/covers to `{job}/viral/`. Cut masters stay in `output/deliverables/`. |

## Active Projects

## Architecture (2026-09-02)

| Stage | Tool |
|-------|------|
| Transcribe | Faster-Whisper + optional Vosk words |
| Plan | **Cursor agent** → manifest.json |
| Assemble | concat_clips.py (multi-clip projects) |
| Render | render_manifest.py / process_stream.py |
| Polish | auto-edit.py (SFX via sfx_resolver + dynamic zoom) |

## Active Projects

### Origin Story (`origin-story`)

- Folder: `projects/0. the origin story/`
- Source: `input/0. Origin story.mp4`
- Transcript: `output/transcript/transcript.txt` (done)
- Approved: `sh01` story-first (100s), `sh02` hook-first (64s), `sh03` hook-first (58s), `sh05` moving-house first-stream `1:03:12–1:03:56` (44s) → `output/deliverables/shorts_approved/`
- Draft: `sh04` Game WITH Life (28s) — splice fails 50s floor and glues two situations
- Chunks: ch01 `04:45–19:45`; ch02 `26:10–38:00` + Tipper `45:31–48:50` (Lebanon skipped). ch03 deferred
- 2026-09-21: shorts floor 50s; never out mid-clause; leftover-theme scan after the brief; compare path must not clobber an existing `_vN`

### Tipper The Story (`tipper-the-story`)

- Folder: `projects/1. tipper the story/`
- Source: `input/1. Tipper _the story_.mp4`
- Transcript: `output/transcript/transcript.txt` (done — do not re-transcribe)
- Planner: `shorts_extraction.md` (nine scripts). Gemini `shorts_instructions.md` is contrast only
- Publish queue: sh05 empathy → sh08 daily journey → sh03 look at what I'm building → sh02 dump everything → sh06 brute force → sh04 push/pull → sh01 eight failed (demoted)
- Parked: sh07 six-months-function, sh09 bootcamp-at-37 (founder memoir, not Tipper people/places/events)
- Chunks: jobs 1+2 rendered (`ch01_common-ground.mp4`, `ch02_show-you-their-world.mp4`). Job 4 under floor. Gemini `chunk_instructions.md` unused.

### Tipper The Origin Story (`tipper-the-origin-story`)

- Folder: `projects/2. tipper the origin story/`
- Entity: **Tipper** (token in the name — not founder `0. the origin story`)
- Source: `input/2. Tipper _the origin_.mp4` (1:14:16)
- Transcript: `output/transcript/transcript.txt` (done — do not re-transcribe)
- Planner: `shorts_extraction.md` (nine) + `chunk_extraction.md` (jobs 1–3)
- Publish queue: sh05 listen → sh01 community → sh06 value-used → sh07 culture → sh04 cab → sh08 SMBs → sh02 competence → sh03 opinion → sh09 birth (demoted)
- Chunks rendered: `ch01_how-value-broke.mp4` (13:09), `ch02_dont-have-an-opinion.mp4` (13:37), `ch03_value-when-used.mp4` (12:10)
- Deferred: job 4 restaurant→birth under 11 min (sh09 only). Job 5 bootcamp park.

### Tipper The Start of the Project (`tipper-the-start-of-the-project`)

- Folder: `projects/6. tipper the start of the project/`
- Entity: **Tipper**. Source `input/6. Tipper _The Start Of The Project_.mp4` (1:06:30). No sidecar `.srt`. Do not re-transcribe.
- Shorts (9): sh03 digitize → sh04 real world → sh05 hormones → sh09 how-people-use → sh07 showing-job → sh06 trash-road → sh01 shovel → sh02 online-problems → sh08 her-business
- Chunks (3): ch01 `08:49–22:36` (827s); ch02 supercut skip THP `39:00–40:16` (666s); ch03 `47:12–1:00:14` (782s). Fourth job under floor / wrong entity.
- Park: partner / $4k / coding / THP name.

### Tipper The Work (`tipper-the-work`)

- Folder: `projects/7. tipper the work/`
- Entity: **Tipper**. Source `input/7. Tipper_ The Work_.mp4` (~1:06:18). No sidecar `.srt`. Do not re-transcribe.
- Publish: sh03 coffee-shop → sh04 talk-to-users → sh06 press-play → sh05 presence → sh07 generate-value → sh08 expand-world → sh09 why-people-use → sh01 look-at-the-world → sh02 trusted-money
- Chunks (3): ch01 `07:26–20:50` (804s); ch02 `22:42–34:40` (718s); ch03 `37:18–49:00` (702s)
- Park: GAF/THP name-drop `03:45–04:57`
- Wall: Whisper 15:25 + shorts 9:32 + chapters 10:57 = **35:54** encode (planning extra)

### Tipper The Effort (`tipper-the-effort`)

- Folder: `projects/8. tipper the effort/`
- Entity: **Tipper**. Source `input/8. Tipper _The Effort_.mp4` (1:03:24). No sidecar `.srt`. Do not re-transcribe.
- Publish: sh03 somewhere-someone → sh01 starts-with-user → sh02 relationship → sh05 where-value → sh06 truth-warped → sh07 shared-world → sh09 create-value → sh08 market → sh04 guitar (demote)
- Chunks (3): ch01 `02:26–15:36` (790s); ch02 `36:58–49:17` (739s); ch03 `49:17–1:00:52` (695s)
- Park: hire/$12k/Africa/UI/friend UX. Ships GAF. Choice/decision leftover. Ego next tape.
- Wall: Whisper 12:52 + shorts 9:36 + chapters 9:01 = **31:29** encode

### Tipper The Change (`tipper-the-change`)

- Folder: `projects/9. tipper the change/`
- Entity: **Tipper**. Source `input/9. Tipper_The_Change.mp4` (1:08:08). No sidecar `.srt`. Do not re-transcribe.
- Publish: sh08 community-chooses-you → sh09 coffee-shop-full → sh04 leave-house → sh03 user-story → sh05 shop-hosts → sh06 talk-to-shop → sh02 lego → sh01 tool → sh07 belong-anywhere
- Chunks (3): ch01 `26:11–40:26` (855s); ch02 `43:18–55:14` (716s); ch03 `55:14–1:06:24` (670s)
- Park: FI / coding-AI / hire / me-thought-it. Whisper 15:38 + shorts 9:23 + chapters 10:27 = **35:28** encode

### GAF Qualifications 1 (`gaf-qualifications-1`)

- Folder: `projects/10 qualifications 1/`. Entity **GAF**. SRT. Do not Whisper.
- Publish: sh07 guild-of-guilds → sh04 accept-failure → sh05 stories-worthy → sh06 entrepreneurial → sh01 jump-in-pool → sh02 shifting-to-gaf → sh03 programs → sh09 i-do-it → sh08 who-is-this-dude
- Chunks (3): ch01 `02:46–14:42` (716s); ch02 `14:42–26:53` (731s); ch03 `26:53–41:24` (871s)
- Park: Tipper diagram `15:54–19:08`. Liberia leftover.

### GAF Qualifications 2 (`gaf-qualifications-2`)

- Folder: `projects/11 qualifications 2/`. Entity **GAF**. SRT. Do not Whisper.
- Publish: sh04 five-percent → sh03 writing → sh08 im-ready → sh09 ready-before-move → sh02 hunting-dark → sh06 environment → sh07 cared-for → sh05 no-chance-wrong → sh01 plant-seeds
- Chunks (3): ch01 `00:24–13:00` (756s); ch02 `28:21–41:19` (778s); ch03 `55:00–1:07:15` (735s)
- Park: dating / scams.

### GAF Qualifications 3 (`gaf-qualifications-3`)

- Folder: `projects/12 qualifications 3/`. Entity **GAF**. SRT. Do not Whisper.
- Publish: sh04 started-the-gaf → sh05 the-gap → sh01 island → sh03 barefoot-to-building → sh08 qualified → sh07 creativity → sh02 no-feedback → sh09 consulting → sh06 note-then-video
- Chunks (2): ch01 `03:06–16:00` (774s); ch02 supercut skip THP `43:03–44:44` (794s). Third under floor.
- Park: THP / Tipper closer.

### Tipper The Social Structures (`tipper-the-social-structures`)

- Folder: `projects/5. tipper the social structures/` (renamed from dump `5. Tipper _The Social Stuctures_`)
- Entity: **Tipper**. Source `input/5. Tipper _The Social Stuctures_.mp4` (58:49, 1280×720). Filename keeps the typo. No sidecar `.srt`. Do not re-transcribe.
- Planner: `shorts_extraction.md` (nine) + `chunk_extraction.md` (jobs 1–4). Gemini `shorts.md` contrast only (two under 50s).
- Publish: sh01 pillars → sh03 hug → sh07 pie → sh08 identity → sh05 vibe → sh02 street → sh06 socially → sh09 communal → sh04 languages
- Chunks: `ch01_leave-the-house.mp4` (12:24), `ch02_three-languages.mp4` (12:32), `ch03_coffee-shop-you-cant-measure.mp4` (12:58), `ch04_same-pillars-on-a-shop.mp4` (12:19)
- Wall: Whisper 13:04 + shorts 9:39 + chapters 13:40 = **36:22** machine.

### Tipper The Startup (`tipper-the-startup`)

- Folder: `projects/4. tipper the startup/` (renamed from dump `4. Tipper _The Startup_`)
- Entity: **Tipper**. Source `input/4. Tipper _The Startup_.mp4` (1:05:11, 1280×720). No sidecar `.srt`. Do not re-transcribe.
- Planner: `shorts_extraction.md` (nine) + `chunk_extraction.md` (jobs 1–4). Gemini `shorts.md` contrast only.
- Publish queue: sh03 commune → sh04 coffee shop → sh09 farmer → sh06 identity → sh07 maps → sh01 create-value → sh05 burnt → sh08 constraints → sh02 don't-force
- Chunks: `ch01_play-the-triangle.mp4` (13:11), `ch02_regulars-occasionals.mp4` (11:03), `ch03_dont-market-random-people.mp4` (14:06), `ch04_ninety-percent-of-the-economy.mp4` (13:12 supercut, skip THP `56:06–56:47`)
- Wall: Whisper 11:43 + shorts 11:25 + chapters 16:33 = **39:41** machine.

### Tipper The Concept (`tipper-the-concept`)

- Folder: `projects/3. tipper the concept/`
- Entity: **Tipper** (token in the name)
- Source: `input/3. Tipper _the concept_.mp4` (1:11:20, 1280×720). No sidecar `.srt` — Whisper this tape. Do not re-transcribe.
- Planner: `shorts_extraction.md` (nine) + `chunk_extraction.md` (jobs 2–5)
- Publish queue: sh03 lettuce → sh05 why-yes → sh07 two-steps → sh09 street → sh08 badge → sh01 sandwich → sh02 value-from-trash → sh04 exchange → sh06 best-not-enough
- Chunks rendered at source size 1280×720: `ch01_four-pains.mp4` (12:43), `ch02_exchange-of-value.mp4` (13:40), `ch03_why-a-restaurant-says-yes.mp4` (12:45), `ch04_value-the-subjective.mp4` (13:14)
- Deferred: job 1 restaurant/trash under 11 min (shorts 01–03). Bootcamp / partner park.
- Wall clock after transcript: shorts 9.4 min (`--jobs 4`), chapters 14.2 min (contiguous, no upscale). Still re-encodes 16:9 (item 6 remux-copy not wired).

### Program Future Ready (`program-future-ready`)

- Folder: `step-1-projects/program future ready vids/` (was `projects/` — operator renamed to step folders 2026-09-23)
- Entity: GAF. Six lectures 13–18 under `lectures/{n}. {Title}/` (mp4 + `.srt` per lecture). Whisper only on locked cut windows. Do not overwrite lecture 13 Whisper clocks.
- Books: `output/ebook/Future-Ready.md` (full) and `Future-Ready-Summary.md` (≥30 pages). Spine pamphlet kept as `Future-Ready-Spine.md`.
- Skill: `skills/lecture_ebook/`. Extraction: `shorts_extraction.md` + `chunk_extraction.md` (jobs unmarked). Queue: `step-1-projects/VIDEO-EDITS.md`. Paused 2026-09-23.
- **Handoff:** when shorts + chunks are done → move whole folder to `step-2-viral-edit/program future ready vids/`.

### hikmat (archived)

- First integration project — timelapse montage, deliverables rendered.
- Assets and config lived under `projects/hikmat/`; no external `~/Desktop/hikmat-project/` dependency.

## THP Cross-References

When editing, consult the **named entity**:

- **THP** — `THP-MEDIA-001`, `THP-MEDIA-003`, `00-brand-core.mdc`
- **Tipper** — GAF brief “GAF and Tipper together”; `THP-TIPPER-BOUNDARY-001`
- **GAF** — `~/Desktop/The G.A.F./GAF_Brand_Brief.md` + brand book
- **founder** (Origin Story) — spoken style only; do not treat as a product queue
