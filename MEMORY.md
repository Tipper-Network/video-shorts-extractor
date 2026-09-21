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
- Transcript: in progress (Whisper `small`)
- Deliverables: shorts + chunks; playback `.md` then extract

### Program Future Ready (`program-future-ready`)

- Folder: `projects/program future ready vids/`
- Entity: GAF. Six lectures 13–18. YouTube `.srt` → titled plains. Whisper only on locked cut windows. Do not overwrite lecture 13 Whisper `transcript.txt`.
- Books: `output/ebook/Future-Ready.md` (full, ~24k) and `Future-Ready-Summary.md` (≥30 pages / ~11k). Spine pamphlet kept as `Future-Ready-Spine.md`.
- Skill: `skills/lecture_ebook/`. Cuts later.

### hikmat (archived)

- First integration project — timelapse montage, deliverables rendered.
- Assets and config lived under `projects/hikmat/`; no external `~/Desktop/hikmat-project/` dependency.

## THP Cross-References

When editing, consult the **named entity**:

- **THP** — `THP-MEDIA-001`, `THP-MEDIA-003`, `00-brand-core.mdc`
- **Tipper** — GAF brief “GAF and Tipper together”; `THP-TIPPER-BOUNDARY-001`
- **GAF** — `~/Desktop/The G.A.F./GAF_Brand_Brief.md` + brand book
- **founder** (Origin Story) — spoken style only; do not treat as a product queue
