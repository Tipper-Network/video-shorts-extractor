---
name: render-manifest
description: Batch-renders all chapters and shorts from an approved manifest.json using FFmpeg. Use after plan-stream or manual manifest edit, when user says render clips, or --mode render.
version: "0.1.0"
status: planned
requires:
  bins: ["python3", "ffmpeg", "ffprobe"]
---

# Render Manifest (Batch Renderer)

**Status: planned** — script not yet implemented. See [planning/roadmap.md](../planning/roadmap.md) Phase 3.

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
python3 content_pipeline/render_manifest.py \
  --manifest content_pipeline/output/{stem}/manifest.json
```

## Workflow

```
1. Validate manifest against planning/schemas/manifest.schema.json
2. Abort if review.status != approved (unless --force)
3. For each chapter → ffmpeg 16:9 cut → output/{stem}/chapters/
4. For each short → ffmpeg 9:16 crop cut → output/{stem}/shorts/
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
- **9:16:** letterbox + blur canvas 1080×1920 (`cut_utils.aspect_filter`)
- **Supercut concat:** `-c copy` (re-encode only if streams mismatch)
- **Shorts:** `--jobs 4` parallel ffmpeg. Chapters stay serial.

## Guardrails

- Never re-transcribe during render
- Log per-clip failures; don't abort entire batch
- Never overwrite a rendered file. Next pass writes `_v2` / `_v3` so both stay for compare. `--force` only when the user asks to replace. Never ffmpeg `-y` onto an existing `_vN` — if `_v2` is taken, write `_v3`.
- Do not render a short whose `script_approved` is false. The agent must paste the playback script and wait.

## Future

- `--auto-editor-tightness` per platform (Phase 6)
