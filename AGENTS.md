# AGENTS.md — Content Pipeline Workspace

This repo is the **cut engine** others clone to onboard. Jobs are local. A website UI is the future front door — same skills, same scripts.

## Purpose

Turn raw footage into two deliverable types:

- **Shorts** — vertical, 9:16
- **Chunks** — horizontal, 16:9, 11–15 min

Cursor + `projects/{name}/` is the current UI (manual drop, agent in-session). Later: website → agent(s) → same `manifest.json` → same ffmpeg. Do not invent a second cut language for the site.

**Git ships the product** (`skills/`, `planning/`, `content_pipeline/`, `_template` folders). **Do not commit** job folders, brand books, or session memory.

**Not in scope:** THP product code, Tipper app, or other repos. Link to them; don't merge.

## Session Startup

Use runtime-provided context first (`AGENTS.md`, `SOUL.md`, `USER.md`, recent `memory/`, `MEMORY.md`).

When working on a **named project**, read its on-disk brief before planning or regenerating frameworks:

1. `projects/{folder}/brief.md` and `requirements.md` — resolve `entity` from the folder/video name ([`skills/entity_brand`](skills/entity_brand/SKILL.md))
2. That entity's file in [`brands/`](brands/) — operator books, not shipped. Founder spoken style is always on (`USER.md` + craft skills).
3. Any `*_instructions.md` or `shorts_extraction.md` in that folder
4. `output/transcript/transcript.txt` if it exists (do not re-transcribe to plan cuts)
5. `output/plan/manifest.json` — update in place; do not recreate from scratch unless asked

Resolve project folder via `project_id` in `pipeline.json` (folder name may differ, e.g. `0. the origin story` → `origin-story`).

Reread files only when the user asks, context is missing, or you need deeper detail.

## Memory

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw session logs
- **User model:** `USER.md` — editing preferences and active-project directives
- **Long-term:** `MEMORY.md` — durable pipeline decisions and lessons

Capture what matters: cut decisions, series state, tooling lessons. Skip secrets unless asked.

### Write It Down

Memory doesn't survive restarts; files do. Before writing, read existing content. Update concretely — no empty placeholders.

- Editing decision worth repeating → `USER.md` or `MEMORY.md`
- Session work log → `memory/YYYY-MM-DD.md`
- Pipeline lesson → relevant skill or `planning/instincts/`

## Red Lines

- Don't exfiltrate private data.
- Don't run destructive commands without asking.
- Prefer `trash` over `rm`.
- Before changing system config (crontab, nginx, etc.), inspect existing state first.
- When in doubt, ask.

## Existing Solutions Preflight

Before building custom tooling, check for maintained open-source options (ffmpeg wrappers, whisper pipelines, auto-editor, etc.). Build custom only when existing tools don't fit. Avoid paid SaaS unless the user approves.

## External vs Internal

**Safe freely:** read files, explore, organize, run local pipeline scripts, work within this workspace (`projects/{name}/input/`, etc.).

**Ask first:** publishing to social platforms, sending emails, anything public, anything uncertain.

## Proactive Work (no ask needed)

- Organize memory files
- Update pipeline docs when behavior changes
- Check `git status` on this workspace
- Review and update `USER.md` / `MEMORY.md` after significant editing sessions

## Key References

| Topic | Location |
|-------|----------|
| Setup & dirs | [`instructions.md`](instructions.md) |
| Orchestrator | [`SKILL.md`](SKILL.md) |
| **Playbooks (visuals + design)** | [`planning/playbooks.md`](planning/playbooks.md) |
| **Flywheel strategies (2 models)** | [`planning/flywheel-strategies.md`](planning/flywheel-strategies.md) |
| **Flywheel visuals** | [`planning/flywheel-strategies-visual.md`](planning/flywheel-strategies-visual.md) |
| Architecture | [`planning/pipeline-architecture.md`](planning/pipeline-architecture.md) |
| **Entity brands (local)** | [`brands/`](brands/) — operator books; `_template.md` is what git ships |
| THP OS (external, series/ops) | `~/Desktop/The-Hard-Port-stuff/The Hard Port/the-hard-port-os/` |
| **Projects (one folder per job)** | [`projects/`](projects/README.md) — jobs gitignored; `_template/` ships |

## Planning Model

**Cursor agent is the planner.** Chapter boundaries, shorts selection, and flywheel tagging happen in-session: read transcript + instincts + skills → write `manifest.json`. No local Ollama server.

Transcription and render stay scripted (Whisper, FFmpeg). Planning is interactive agent work.

## Local Notes

```markdown
- Git = onboardable product. Jobs/brands/memory = operator data (website accounts later).
- Projects root: projects/{name}/ — input, output, config, *_instructions.md
- Agent reads: brief.md → requirements.md → brands/{entity} → *_instructions.md → transcript.txt → manifest.json
```
