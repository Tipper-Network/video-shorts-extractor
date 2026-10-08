# Pipeline Modules — Callable Actions

Each module is **one independently invokable action**. Projects enable/disable modules via `pipeline.json`. Scripts live under [`../cli/`](../cli/) and [`../lib/`](../lib/) — see [`../README.md`](../README.md).

## Design principle

```
SKILL (rules)  +  MODULE (script)  +  PROJECT CONFIG (pipeline.json)  =  RUN
```

## Module catalog

| Module | Script | Input | Output |
|--------|--------|-------|--------|
| **concat** | `cli/concat_clips.py` | raw clip folder | master mp4 |
| **transcribe** | `cli/process_stream.py --mode transcribe` | video | `output/transcript/` |
| **detect_topics** | `cli/detect_topics.py` | transcript json | `{stem}.topics.json` |
| **plan_manifest** | Cursor agent (no script) | transcript + topics + skills | `manifest.json` |
| **compose_shorts** | `cli/compose_shorts.py` | clip-map.json | segment-pool + manifest |
| **render** | `cli/render_manifest.py` | manifest.json | `chapters/` + `shorts/` |
| **trim_silence** | `lib/trim_silence.py` | single mp4 | trimmed mp4 |
| **polish** | `cli/auto_edit.py` | rendered clips | SFX + zoom pass |
| **viral_captions** | `cli/viral_captions.py` | cut short + words | `viral/shorts/` |

## Invoke one module

```bash
python3 content_pipeline/cli/run_module.py --project origin-story --module render \
  -- --manifest "step-2-viral-edit/0. the origin story/output/plan/manifest.json"

# or shim
python3 content_pipeline/run_module.py --project origin-story --module detect_topics -- \
  --transcript …
```

## Cut modes / trim

See playbooks and `lib/trim_profiles.py`. Skip trim with `--no-trim` on render.
