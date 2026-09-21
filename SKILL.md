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

**Product vs operator:** this repo is the engine. Brand books live in local `brands/` (template in git). Do not merge THP/Tipper/GAF product repos here.

## Standard Directory Map

- **Raw Input:** `content_pipeline/input/` (or linked external folder)
- **Extracted Audio:** `content_pipeline/audio/`
- **Transcripts & JSON:** `content_pipeline/subtitles/`
- **Final Output:** `content_pipeline/output/`
- **Series State:** `content_pipeline/series/`
- **Execution Script:** `content_pipeline/process_stream.py`

## Operational Routing

When receiving a request to process video:

1. **Entity:** Resolve Tipper / THP / GAF / founder from the video or folder name. Read [`skills/entity_brand/`](skills/entity_brand/SKILL.md) and that entity's brand records before planning cuts.
2. **Target Identification:** If the user specifies a platform (TikTok, Instagram, YouTube), defer to `skills/<platform>/SKILL.md`.
3. **Default Fallback:** No platform specified → one **11-15 min mid-form chunk** (16:9) + **2 vertical shorts** (9:16).
4. **Storyline context:** Read `brands/{entity}` for the named job. Operator pack on this machine: THP → `the-hard-port-brief.md`, Tipper → `Tipper_Brand_Book.md`, GAF → brief + book.
5. **Execution:** Run pipeline scripts — never expect scripts to plan cuts autonomously.
6. **Leftover scan:** After instruction-file themes are scripted, read the rest of the transcript. The brief is not a cap. Note unused situation→resolve blocks before calling the job done.

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
| [`skills/chunks/`](skills/chunks/SKILL.md) | 11–15 min mid-form chunks |
| [`skills/entity_brand/`](skills/entity_brand/SKILL.md) | Title = brand key: Tipper / THP / GAF / founder |
| [`skills/situation_resolve/`](skills/situation_resolve/SKILL.md) | One situation (problem/issue/struggle/intention) held until it resolves |
| [`skills/extract_shorts/`](skills/extract_shorts/SKILL.md) | Hook → Setup → Resolution + coherence gate |
| [`skills/vertical_shorts/`](skills/vertical_shorts/SKILL.md) | 9:16 vertical shorts (editorial versions, not platforms) |

## Guardrails

- Verify input file exists before running scripts.
- Keep matching base filenames across audio, subtitles, and output for tracking.
- For multi-clip requests: consult `planning/` first — do not expect single-clip `process_stream.py` to produce chapters + shorts.
- Chronological clip collections (e.g. hikmat): use `concat_clips.py --mode draft` first; normalize only for export.
- Never block chat on ffmpeg — background long transcodes and report progress.
