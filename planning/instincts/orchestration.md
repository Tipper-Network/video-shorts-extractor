# Instincts: Orchestration

For the Orchestrator agent coordinating pipeline runs.

## Routing

- **Always** check `content_pipeline/input/` for file existence before any processing.
- **If** user names a platform → load `skills/{platform}/SKILL.md` and pass its parameters downstream.
- **If** no platform specified → default per vision.md: all chapters + minimum 2 flywheel shorts.
- **Never** run render without an approved manifest (human or QA PASS).

## Delegation

- **Always** delegate transcription, planning, and rendering to specialized roles — don't inline their logic.
- **Always** run chapter and shorts planning as Cursor agent work (read transcript + instincts → write manifest) — not via local Ollama.
- **Prefer** reusing existing transcript if input mtime ≤ transcript mtime (skip re-transcribe).
- **Always** report a summary table at end: chapters count, shorts count, output paths, any failures.

## Modes

| Mode | Actions |
|------|---------|
| `plan` | Transcribe (if needed) → plan → write manifest → stop |
| `render` | Validate manifest → render only |
| `full` | plan → review gate → render |

- **Default** to `plan` until render script is shipped and user opts into `full`.

## Long-Running Shell

- **Never** wait synchronously on ffmpeg/transcribe jobs expected to exceed ~30 seconds.
- **Always** background long jobs (`block_until_ms: 0`), print the exact command, and tell the user how to check progress.
- **Prefer** `concat_clips.py --dry-run` before committing to normalize passes.

## Errors

- **Never** hide partial failures — list which clips succeeded and which failed.
- **Always** preserve intermediate artifacts (audio, transcript) on failure for debugging.
- **Prefer** actionable error messages ("transcript missing — run transcribe first") over generic stack traces to user.

## Planning Folder

- **Always** consult `planning/roadmap.md` for current phase before implementing new behavior.
- **Prefer** updating roadmap status when shipping a phase.
