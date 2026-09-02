---
name: plan-stream
description: Plans multi-clip output from long streams — full transcription, themed chapter segmentation, and flywheel-tagged shorts. Writes manifest.json. Use when processing 2hr streams, multi-chapter splits, or before batch render.
version: "0.2.0"
status: planned
requires:
  bins: ["python3", "ffmpeg", "ffprobe"]
---

# Plan Stream (Multi-Clip Planner)

**Status: planned** — Cursor agent plans in-session; transcribe orchestration script optional. See [planning/roadmap.md](../planning/roadmap.md) Phase 2.

**Planner:** Cursor agent (not Ollama). Agent reads transcript, applies instincts, writes manifest.

## When to Use

- Input is 30+ minutes and may contain multiple topics
- User wants themed chapters (10–30 min) and/or flywheel shorts
- Before `render-manifest` — produces the manifest contract

## Agent Roles

- [Transcriber](../planning/agents/transcriber.md)
- [Chapter Planner](../planning/agents/chapter-planner.md)
- [Shorts Planner](../planning/agents/shorts-planner.md)

## Instincts

Read before planning:
- [content-pipeline](../planning/instincts/content-pipeline.md)
- [llm-planning](../planning/instincts/llm-planning.md)

## Target Command

```bash
python3 content_pipeline/plan_stream.py \
  --input {filename}.mp4 \
  --series {series_id} \
  --episode {n}
```

## Workflow

```
1. Verify input in content_pipeline/input/
2. Transcribe full video → subtitles/{stem}.json
3. Cursor agent: block-label transcript (~5–10 min chunks)
4. Cursor agent: merge blocks into chapters (600–1800s) — skills/youtube-chunks rules
5. Cursor agent: plan shorts per chapter with flywheel tags — skills/youtube-shorts + flywheel-series
6. Write content_pipeline/output/{stem}/manifest.json
7. Set review.status = draft — stop for human/QA approval
```

## Output Schema

[planning/schemas/manifest.schema.json](../planning/schemas/manifest.schema.json)

Example: [planning/templates/manifest.example.json](../planning/templates/manifest.example.json)

## Platform Deference

| User request | Load skill |
|--------------|------------|
| YouTube chapters | youtube-chunks |
| YouTube Shorts | youtube-shorts |
| TikTok | tiktok-shorts |
| Instagram | instagram-reels |

## Guardrails

- Never truncate transcript to 150 segments
- Never skip manifest write
- Never set review.status = approved without human or QA PASS
