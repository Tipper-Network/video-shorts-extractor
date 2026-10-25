---
name: render-manifest
description: Batch-renders all chapters and shorts from an approved manifest.json using FFmpeg. Use after plan-stream or manual manifest edit, when user says render clips, or --mode render.
version: "1.0.0"
status: active
requires:
  bins: ["python3", "ffmpeg", "ffprobe"]
---

# Render Manifest (Batch Renderer)

**Status: active.** Implementation is `content_pipeline/cli/render_manifest.py`. It calls `render_clip_entry` in `content_pipeline/lib/cut_utils.py`. Edit map: [`../edit/SKILL.md`](../edit/SKILL.md).

## When to Use

- `manifest.json` exists and `review.status` is `approved`
- User requests render without re-planning
- Orchestrator `--mode render` or post-QA PASS

## Agent Role

- [Renderer](../planning/agents/renderer.md)

## Instincts

- [content-pipeline](../planning/instincts/content-pipeline.md) — Rendering section

## Target Command

```bash
python3 content_pipeline/cli/render_manifest.py \
  --manifest "projects/{name}/output/plan/manifest.json" \
  --project {project_id}
```

## Workflow

```
1. Validate manifest against planning/schemas/manifest.schema.json
2. Abort if review.status != approved (unless --force)
3. For each chapter → ffmpeg 16:9 cut → output/{stem}/chapters/
4. For each short → `aspect_filter("9:16")` blur stack, not a crop → `output/deliverables/shorts/`
5. Update manifest rendered flags + output_file paths
6. Generate publish_queue.csv from shorts publish_order + chapters
```

## Output Layout

```
content_pipeline/output/{stem}/
  manifest.json          (updated with rendered flags)
  chapters/
    youtube_ch01_slug.mp4
  shorts/
    yt-shorts_sh01_slug.mp4
  publish_queue.csv
```

## FFmpeg Filters

- **16:9:** `scale='min(1920,iw)':-2` — never upscale
- **9:16:** `aspect_filter` — blurred 1080×1920 ground, original scaled to 1080 wide and centered. Not a face crop.
- **Supercut concat:** `-c copy` (re-encode only if streams mismatch)
- **Shorts:** `--jobs 4` parallel ffmpeg. Chapters stay serial.

## Guardrails

- Never re-transcribe during render
- Log per-clip failures; don't abort entire batch
- Never overwrite a rendered file. Next pass writes `_v2` / `_v3` so both stay for compare. `--force` only when the user asks to replace. Never ffmpeg `-y` onto an existing `_vN` — if `_v2` is taken, write `_v3`.
- Do not render a short whose `script_approved` is false. The agent must paste the playback script and wait.

## Future

- `--auto-editor-tightness` per platform (Phase 6)
