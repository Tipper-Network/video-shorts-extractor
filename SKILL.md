---
name: content-pipeline-master
description: Master orchestration skill for local video editing and content creation pipelines.
version: "1.0.0"
requires:
  bins: ["python3", "ffmpeg", "ffprobe", "auto-editor"]
---

# Master Content Pipeline Controller

## Overview

This workspace handles local video processing into multi-platform clips using Faster-Whisper, FFmpeg, and **Cursor agent planning** (chapters, shorts, manifests).

**Separate from THP:** brand strategy, series scripts, and editorial voice live in `The-Hard-Port-stuff/the-hard-port-os/`. This workspace executes the cut.

## Standard Directory Map

- **Raw Input:** `content_pipeline/input/` (or linked external folder)
- **Extracted Audio:** `content_pipeline/audio/`
- **Transcripts & JSON:** `content_pipeline/subtitles/`
- **Final Output:** `content_pipeline/output/`
- **Series State:** `content_pipeline/series/`
- **Execution Script:** `content_pipeline/process_stream.py`

## Operational Routing

When receiving a request to process video:

1. **Target Identification:** If the user specifies a platform (TikTok, Instagram, YouTube), defer to `skills/<platform>/SKILL.md`.
2. **Default Fallback:** No platform specified → one **15-minute YouTube chapter** (16:9) + **2 vertical shorts** (9:16).
3. **Storyline context:** If the content belongs to a THP series, read the relevant script from THP `content/youtube/` for tone and structure — apply cuts here.
4. **Execution:** Run pipeline scripts — never expect scripts to plan cuts autonomously.

## Pipeline Scripts

| Script | When |
|--------|------|
| `concat_clips.py` | Multi-clip chronological assembly |
| `process_stream.py --mode transcribe` | Extract transcript |
| `process_stream.py --mode render` | Cut from manifest or manual timestamps |
| `render_manifest.py` | Batch render approved manifest |
| `auto-edit.py` | SFX + zoom polish pass |

## Planning Hub

Design, agent roles, instincts, schemas, and roadmap: [`planning/`](planning/README.md).

Multi-clip pipeline (plan → review → render) is spec'd there. Current code (`process_stream.py`) is single-clip v0.

## Pipeline Skills

| Skill | Status | Purpose |
|-------|--------|---------|
| [`skills/plan_stream/`](skills/plan_stream/SKILL.md) | planned | Full plan → manifest.json |
| [`skills/render_manifest/`](skills/render_manifest/SKILL.md) | planned | Batch render from manifest |
| [`skills/flywheel_series/`](skills/flywheel_series/SKILL.md) | planned | Series + flywheel continuity |

## Editing Skills (shipped)

| Skill | Purpose |
|-------|---------|
| [`skills/dynamic_zoom/`](skills/dynamic_zoom/SKILL.md) | Periodic zoom in/out |
| [`skills/sfx_allocation/`](skills/sfx_allocation/SKILL.md) | Word-triggered SFX |
| [`skills/youtube_chunks/`](skills/youtube_chunks/SKILL.md) | 10–30 min chapters |
| [`skills/youtube_shorts/`](skills/youtube_shorts/SKILL.md) | Vertical teasers |
| [`skills/tiktok_shorts/`](skills/tiktok_shorts/SKILL.md) | Fast-paced shorts |
| [`skills/instagram_reels/`](skills/instagram_reels/SKILL.md) | Visual story reels |

## Guardrails

- Verify input file exists before running scripts.
- Keep matching base filenames across audio, subtitles, and output for tracking.
- For multi-clip requests: consult `planning/` first — do not expect single-clip `process_stream.py` to produce chapters + shorts.
- Chronological clip collections (e.g. hikmat): use `concat_clips.py --mode draft` first; normalize only for export.
- Never block chat on ffmpeg — background long transcodes and report progress.
