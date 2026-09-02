# Instincts: Agent Planning

For Chapter Planner and Shorts Planner roles — executed by the **Cursor agent** in-session (not a local Ollama API).

## Prompt Design

- **Always** request raw JSON only — no markdown fences in the ideal case; clean them if present.
- **Never** ask for "pick the best clip" when the task is segmentation — ask for **all** viable segments.
- **Prefer** focused single-purpose passes over one mega-prompt for a 2hr stream.
- **Always** include duration constraints explicitly in seconds (600, 1800, 30, 60).

## Context Management

- **Never** skip reading the full transcript file — load and chunk it yourself across turns if needed.
- **Prefer** map-reduce: block labels first, merge second, refine boundaries third.
- **Always** pass compact transcript format: `[start s - end s] text` per line when reasoning over blocks.
- **Prefer** 5–10 minute blocks for the labeling pass.

## Output Validation

- **Always** parse JSON defensively; on failure, retry once with stricter format instruction.
- **Never** silently accept fallback timestamps without logging a warning.
- **Always** clamp start/end to valid video duration after planning.
- **Always** write results to `manifest.json` matching [manifest.schema.json](../schemas/manifest.schema.json).

## Planner Identity

- **Default:** Cursor agent in this workspace session.
- **Always** set `planner_model` in manifest to `"cursor-agent"` (or note the Cursor model slug if known).
- **Never** assume a local Ollama server — removed 2026-09-02.

## Quality Signals

When reviewing planner output, reject if:

- Chapter title doesn't match transcript content at that timestamp
- Short hook is generic ("great tip") without specific content reference
- Two chapters claim the same time range
- Flywheel stage doesn't match clip content (e.g. "referral" with no result mentioned)
