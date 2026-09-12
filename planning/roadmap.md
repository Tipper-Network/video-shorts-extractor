# Roadmap

Track status here. Update checkboxes as phases ship.

## Phase 0 — Foundation (shipped)

- [x] Directory layout (`input/`, `audio/`, `subtitles/`, `output/`)
- [x] Single-clip pipeline (`process_stream.py`)
- [x] Platform skill stubs (youtube-chunks, youtube-shorts, tiktok, instagram)
- [x] Planning hub (`planning/`)
- [x] Project folder pattern (`content_pipeline/projects/`)
- [x] Capability test matrix (`planning/capability-matrix.md`)
- [x] First integration project: **hikmat**

## Phase 1 — Schemas & Contracts

- [ ] Finalize `manifest.schema.json` and `series.schema.json`
- [ ] Add example templates under `planning/templates/`
- [ ] Document manifest field meanings in schema descriptions

**Exit:** Can hand-write a valid manifest and know what render expects.

## Phase 2 — Plan Workflow (Cursor Agent)

- [ ] Document Cursor-agent planning workflow in `skills/plan_stream/SKILL.md`
- [ ] Full-transcript path (remove 150-segment cap from legacy script)
- [ ] Block summarization pass (Cursor agent, map-reduce)
- [ ] Chapter merge pass (Cursor agent)
- [ ] Shorts planning pass with flywheel tags (Cursor agent)
- [ ] Write `output/{stem}/manifest.json`
- [ ] Optional: `plan_stream.py` for transcribe-only orchestration (no Ollama)

**Exit:** Agent produces editable manifest from a long stream transcript.

## Phase 3 — Render Script

- [x] Create `content_pipeline/render_manifest.py`
- [x] Batch ffmpeg from manifest entries
- [x] Create `content_pipeline/concat_clips.py` (multi-clip assembly)
- [ ] Respect per-clip aspect, min/max, target prefix (partial)
- [ ] Generate `publish_queue.csv` from manifest
- [x] Skill: `skills/render_manifest/SKILL.md` (script shipped)

**Exit:** Render all clips from approved manifest without re-transcribing.

## Phase 4 — Series & Flywheel

- [ ] Create `content_pipeline/series/` directory
- [ ] Read/write series state in planner
- [ ] Auto-advance flywheel stage across episodes
- [ ] Skill: `skills/flywheel-series/SKILL.md`

**Exit:** Episode 3 shorts continue theme and stage from episode 2.

## Phase 5 — Agent Automation

- [ ] Wire orchestrator to invoke plan → review gate → render
- [ ] QA reviewer agent validates manifest against schemas + instincts
- [ ] Optional: Cursor hook or watcher for "drop file in input/"

## Phase 6 — Polish (later)

- [ ] auto-editor silence removal per platform tightness
- [ ] Burned-in subtitles
- [ ] GPU Whisper (`cuda`)
- [ ] Face-tracking crop for 9:16

## Current Priority

**Origin Story flywheel** — transcribe → manifest validation → render shorts + chapters.  
Track in [`capability-matrix.md`](capability-matrix.md). Project brief: [`../projects/0. the origin story/brief.md`](../projects/0.%20the%20origin%20story/brief.md).

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-09-01 | Plan → review → render (not one-shot) | Human QA cheaper than bad ffmpeg burns |
| 2026-09-01 | Map-reduce for chapters | 2hr transcript exceeds LLM context |
| 2026-09-01 | Separate plan + render scripts | Clear handoff, reusable transcripts |
| 2026-09-02 | Cursor agent replaces Ollama for planning | Interactive review beats blind local LLM |
| 2026-09-02 | On-demand SFX via sfx_resolver | No local asset library; API + synthetic fallback |
| 2026-09-02 | concat_clips.py for multi-clip projects | hikmat-style chronological assembly |
| 2026-09-02 | Project vs platform separation | `projects/{name}/requirements.md` per job; skills/code shared |
