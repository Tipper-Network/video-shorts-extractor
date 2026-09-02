# MEMORY.md — Pipeline Decisions

Durable facts and decisions for the content pipeline workspace. Not user preferences (those go in `USER.md`).

## Workspace Scope (2026-09-02)

This workspace is the **local video editing and content creation pipeline** — separate from:

- **THP** (`~/Desktop/The-Hard-Port-stuff/The Hard Port/the-hard-port-os/`) — brand strategy, series scripts, editorial voice
- **Tipper** and other product repos — application code

THP defines *what* to say. This workspace defines *how* to cut and render.

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

### hikmat

- Raw clips: `~/Desktop/hikmat-project/` (11 clips)
- Timeline: `content_pipeline/output/hikmat/hikmat_timeline.mp4` — **concat done**
- Next: transcribe → agent storyline review → polish

## THP Cross-References

When editing THP-branded content, consult:

- `THP-MEDIA-001` — YouTube attraction architecture
- `THP-MEDIA-003` — Visual and editorial system
- `the-hard-port-os/content/youtube/` — series scripts and observation bank
