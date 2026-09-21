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

### hikmat (archived)

- First integration project — timelapse montage, deliverables rendered.
- Assets and config lived under `projects/hikmat/`; no external `~/Desktop/hikmat-project/` dependency.

## THP Cross-References

When editing, consult the **named entity**:

- **THP** — `THP-MEDIA-001`, `THP-MEDIA-003`, `00-brand-core.mdc`
- **Tipper** — GAF brief “GAF and Tipper together”; `THP-TIPPER-BOUNDARY-001`
- **GAF** — `~/Desktop/The G.A.F./GAF_Brand_Brief.md` + brand book
- **founder** (Origin Story) — spoken style only; do not treat as a product queue
