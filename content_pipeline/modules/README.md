# Pipeline Modules — Callable Actions

Each module is **one independently invokable action**. Projects enable/disable modules via `projects/{id}/pipeline.json`. The agent (or you) composes modules into a workflow per video.

## Design principle

```
SKILL (rules)  +  MODULE (script)  +  PROJECT CONFIG (pipeline.json)  =  RUN
```

- **Skills** (`skills/`) — platform rules (duration, hook, trim level)
- **Project skills** (`projects/{id}/skills/`) — overrides per job
- **Modules** (this catalog) — executable actions
- **pipeline.json** — which modules apply, cut modes, flywheel on/off

Layer modules to build flywheel sequences: transcribe → detect topics → plan chapters → plan shorts per stage → render → polish.

## Module catalog

| Module | Script | Input | Output |
|--------|--------|-------|--------|
| **concat** | `concat_clips.py` | raw clip folder | master mp4 |
| **transcribe** | `process_stream.py --mode transcribe` | video | `subtitles/{stem}.json` |
| **detect_topics** | `detect_topics.py` | transcript json | `{stem}.topics.json` |
| **plan_manifest** | Cursor agent (no script) | transcript + topics + skills | `manifest.json` |
| **compose_shorts** | `compose_shorts.py` | clip-map.json | segment-pool + manifest |
| **render** | `render_manifest.py` | manifest.json | `chapters/` + `shorts/` |
| **trim_silence** | `trim_silence.py` | single mp4 | trimmed mp4 |
| **polish** | `auto-edit.py` / `--polish` | rendered clips | SFX + zoom pass |

## Invoke one module

```bash
# Generic runner (checks pipeline.json enabled flag)
python3 content_pipeline/run_module.py --project origin-story --module render \
  -- --manifest "projects/0. the origin story/output/plan/manifest.json"

# Direct call (always works)
python3 content_pipeline/detect_topics.py \
  --transcript content_pipeline/subtitles/episode.json \
  --project my-series
```

## Auto topic detection (two layers)

| Layer | Who | What |
|-------|-----|------|
| **1 — heuristic** | `detect_topics.py` | Pause boundaries + lexical shift → blocks + chapter **candidates** |
| **2 — agent** | Cursor in-session | Titles, themes, sentence-safe boundaries → `manifest.json` chapters[] |

Heuristic output is never final — always `needs_agent_review`. Agent reads `{stem}.topics.json` + full transcript.

```bash
python3 content_pipeline/detect_topics.py \
  --transcript content_pipeline/subtitles/my_episode.json \
  --output content_pipeline/output/my_episode/my_episode.topics.json
```

## Cut modes (per project + per clip)

| Mode | Use case | Manifest shape |
|------|----------|------------------|
| **contiguous** | Speech chapters, single-clip shorts | `start`, `end` |
| **supercut** | Timelapse montage, topic highlights reel | `segments[]`, optional `cut_mode: "supercut"` |

Set defaults in `pipeline.json`:

```json
"chapters": { "cut_mode": "contiguous" },
"shorts":   { "cut_mode": "supercut" }
```

Override per clip in manifest:

```json
{
  "id": "ch01",
  "cut_mode": "supercut",
  "title": "Best onboarding moments",
  "segments": [
    { "start": 120, "end": 145, "label": "hook" },
    { "start": 890, "end": 920, "label": "payoff" }
  ]
}
```

## Silence / filler trim on render

Trim runs **after each cut** when `render.trim_on_render: true`.

| Level | Source skill | Method |
|-------|--------------|--------|
| `off` | hikmat, silent video | skip |
| `light` | youtube-chunks | ffmpeg, gaps > 2.5s |
| `moderate` | youtube-shorts, reels | auto-editor 0.6s margin |
| `aggressive` | tiktok-shorts | auto-editor 0.4s margin |

Resolution order: clip `trim` field → manifest `render.default_trim` → project `chapters/shorts.default_trim` → platform target default.

```bash
# Skip trim for one run
python3 content_pipeline/render_manifest.py --manifest ... --no-trim
```

## Example workflows

### THP talking-head episode (flywheel)

```json
"workflow": ["transcribe", "detect_topics", "plan_manifest", "render", "polish"]
```

Agent: detect topics → plan chapters (contiguous) → plan shorts per flywheel stage → render with trim.

### Hikmat timelapse (no flywheel)

```json
"workflow": ["concat", "compose_shorts", "render"]
```

Visual montage shorts only; detect_topics off; trim off.

### Topic supercut chapter (highlights reel)

```json
"chapters": { "cut_mode": "supercut", "default_trim": "moderate" }
```

Agent picks non-adjacent segments exploring one theme → `segments[]` in chapter entry.

## Project setup

```bash
cp content_pipeline/projects/_template/pipeline.json \
   content_pipeline/projects/my-project/pipeline.json
# Edit modules + cut_mode + flywheel
```

See [`planning/modular-pipeline.md`](../../planning/modular-pipeline.md) for flywheel layering strategy.
