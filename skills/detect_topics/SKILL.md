---
name: detect-topics
description: Heuristic topic block detection from full Whisper transcript. Produces chapter candidates for agent review — Layer 1 before manifest planning.
version: "1.0.0"
requires:
  bins: ["python3"]
---

# Detect Topics (Layer 1)

## When to Use

- After `transcribe` — full `subtitles/{stem}.json` exists
- Before agent writes `manifest.json` chapters
- Disabled for silent/visual-only projects (set in `pipeline.json`)

## When NOT to Use

- No speech (hikmat timelapse) → use `compose_shorts` instead
- `detect_topics.method: agent-only` in pipeline.json → agent reads raw transcript only

## Command

```bash
python3 content_pipeline/detect_topics.py \
  --transcript content_pipeline/subtitles/{stem}.json \
  --output content_pipeline/output/{stem}/{stem}.topics.json \
  --project {series_id}
```

Or via module runner:

```bash
python3 content_pipeline/run_module.py --project my-series --module detect_topics -- \
  --transcript content_pipeline/subtitles/episode.json
```

## Output

`{stem}.topics.json`:

| Field | Purpose |
|-------|---------|
| `blocks[]` | ~pause-delimited speech chunks with preview text |
| `boundaries[]` | Scored topic shift points (lexical + pause) |
| `chapter_candidates[]` | Merged 10–30 min windows — **needs agent review** |

## Agent Layer 2 (required)

Agent reads topics file + full transcript + `skills/chunks/`:

1. Assign chapter titles and themes
2. Snap start/end to sentence boundaries (+10s context)
3. Split or merge candidates outside 600–1800s
4. Write `manifest.json` chapters[] — contiguous or supercut per project config
5. Plan shorts from hook windows inside each chapter

## Parameters (pipeline.json)

```json
"detect_topics": {
  "enabled": true,
  "method": "heuristic",
  "pause_threshold_sec": 2.5
},
"chapters": {
  "min_sec": 600,
  "max_sec": 1800
}
```

## Guardrails

- Never treat chapter_candidates as final — always agent review
- Never truncate transcript before detection
- Prefer contiguous chapters unless project sets `cut_mode: supercut`
