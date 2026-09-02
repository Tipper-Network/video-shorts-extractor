# Pipeline Architecture — Plan → Review → Render

## Current State (v0)

`process_stream.py` runs a linear single-clip pipeline (legacy):

```
video → audio → whisper → ollama (1 clip) → ffmpeg → 1 output
```

**Legacy note:** v0 still calls Ollama for a single clip. Ollama is **removed from the stack** — do not extend this path. Use Cursor agent planning + manifest render for new work.

**Blockers for multi-clip (v0):**
- Legacy script receives only first ~150 transcript segments
- Returns single `{start, end, title}` object
- No manifest, no series state, no batch render

## Target State (v1)

```
                    ┌─────────────────┐
  input/*.mp4 ─────►│  TRANSCRIBER    │──► subtitles/{stem}.json
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ CHAPTER PLANNER │──► block summaries → merge themes
                    │ (Cursor agent)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ SHORTS PLANNER  │──► flywheel tags + parent chapter
                    │ (Cursor agent)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ manifest.json   │◄── human edit (optional)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    RENDERER     │──► chapters/ + shorts/
                    └─────────────────┘
```

## Stage Details

### 1. Transcriber

- **Input:** `content_pipeline/input/{file}.mp4`
- **Output:** `content_pipeline/subtitles/{stem}.json`, `content_pipeline/audio/{stem}.wav`
- **Tool:** Faster-Whisper (full file, no truncation)
- **Agent:** [agents/transcriber.md](agents/transcriber.md)

### 2. Chapter Planner

- **Input:** Full transcript JSON
- **Method:** Map-reduce over ~5–10 min blocks
  1. Label each block: topic, energy, topic-start vs continuation
  2. Merge adjacent same-topic blocks until 600–1800s
  3. Snap boundaries to sentence edges (+ 10s context guard)
- **Output:** `chapters[]` in manifest
- **Rules:** [skills/youtube-chunks/SKILL.md](../skills/youtube-chunks/SKILL.md)
- **Agent:** [agents/chapter-planner.md](agents/chapter-planner.md)

### 3. Shorts Planner

- **Input:** Transcript + chapters[] + series state
- **Method:** Per chapter, extract 1–2 moments; assign flywheel stage; write CTA teasing parent chapter
- **Output:** `shorts[]` in manifest
- **Rules:** Platform skills under `skills/youtube-shorts/`, `tiktok-shorts/`, etc.
- **Agent:** [agents/shorts-planner.md](agents/shorts-planner.md)

### 4. Manifest (contract)

- **Schema:** [schemas/manifest.schema.json](schemas/manifest.schema.json)
- **Human gate:** Review/edit before render until QA agent is reliable
- **Location:** `content_pipeline/output/{stem}/manifest.json`

### 5. Renderer

- **Input:** Approved manifest
- **Method:** Loop ffmpeg cuts; apply aspect/duration per clip entry
- **Output:**
  ```
  output/{stem}/
    manifest.json
    chapters/
    shorts/
    publish_queue.csv   (optional)
  ```
- **Agent:** [agents/renderer.md](agents/renderer.md)

### 6. Series State (flywheel continuity)

- **Schema:** [schemas/series.schema.json](schemas/series.schema.json)
- **Location:** `content_pipeline/series/{series_name}.json`
- Tracks: theme, episode number, last flywheel stage, published clip IDs

## Agent Planning Strategy

Planning runs **in Cursor** — not via a local Ollama server. The agent reads the full transcript (map-reduce across blocks if needed), applies instincts and platform skills, and writes `manifest.json`.

| Pass | Scope | Focus |
|------|-------|-------|
| Block label | ~5–10 min of transcript | Topic name, start/continuation, hook score |
| Chapter merge | Block labels only | Merge into 600–1800s segments with titles |
| Short pick | One chapter's segments | Flywheel stage, hook, CTA, 30–60s window |

**Never** one-shot "analyze entire 2hr stream" in a single skim — chunk and iterate for quality.

## Script Split (recommended)

| Script | Mode | Status |
|--------|------|--------|
| `plan_stream.py` | `--mode plan` | planned |
| `render_manifest.py` | `--mode render` | planned |
| `process_stream.py` | legacy single-clip | shipped (deprecate after v1) |

## Orchestrator

[agents/orchestrator.md](agents/orchestrator.md) coordinates the full run, routes to platform skills, and enforces guardrails from [instincts/content-pipeline.md](instincts/content-pipeline.md).
