# AGENTS.md — Content Pipeline Workspace

This workspace is home for **local video editing and content creation**. Treat it that way.

## Purpose

Turn raw footage into publishable, platform-ready content:

- Transcribe, plan cuts, apply editing skills, render
- Maintain series continuity and flywheel sequencing
- Keep strategy in THP; keep execution here

**Not in scope:** THP product code, Tipper app, or other repos. Link to them; don't merge.

## Session Startup

Use runtime-provided context first (`AGENTS.md`, `SOUL.md`, `USER.md`, recent `memory/`, `MEMORY.md`).

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

**Safe freely:** read files, explore, organize, run local pipeline scripts, work within this workspace and linked input folders (e.g. `~/Desktop/hikmat-project/`).

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
| THP strategy (external) | `~/Desktop/The-Hard-Port-stuff/The Hard Port/the-hard-port-os/` |
| Platform rules | [`skills/`](skills/) |

## Planning Model

**Cursor agent is the planner.** Chapter boundaries, shorts selection, and flywheel tagging happen in-session: read transcript + instincts + skills → write `manifest.json`. No local Ollama server.

Transcription and render stay scripted (Whisper, FFmpeg). Planning is interactive agent work.

## Local Notes

```markdown
- Projects root: projects/{name}/ — input, output, config, skills all in one folder
- Hikmat: projects/hikmat/ — see projects/hikmat/FOLDERS.md
- THP content scripts: ~/Desktop/The-Hard-Port-stuff/The Hard Port/the-hard-port-os/content/youtube/
- SFX keys (optional): FREESOUND_API_KEY, PIXABAY_API_KEY — see content_pipeline/.env.example
- Vosk model: VOSK_MODEL_PATH for word-level SFX triggers
```
