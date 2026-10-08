# Content pipeline — engine code

**CLI = verbs you run. Lib = shared guts. Config = knobs.**

Old flat paths still work via thin shims at this folder’s root
(`python3 content_pipeline/render_manifest.py …`).

```text
content_pipeline/
├── cli/                 ← entry points (run these)
│   ├── process_stream.py
│   ├── render_manifest.py
│   ├── concat_clips.py
│   ├── detect_topics.py
│   ├── compose_shorts.py
│   ├── auto_edit.py
│   ├── viral_captions.py
│   ├── viral_zoom.py
│   └── run_module.py
├── lib/                 ← imported by cli (not usually run alone)
│   ├── project_paths.py
│   ├── project_config.py
│   ├── cut_utils.py
│   ├── transcribe.py
│   ├── srt_to_text.py
│   ├── trim_silence.py
│   ├── trim_profiles.py
│   ├── pipeline_log.py
│   ├── sfx_resolver.py
│   └── env_loader.py
├── config/              ← JSON + .env.example
│   ├── sfx_triggers.json
│   ├── censor_words.json
│   └── .env.example
├── _root.py             ← PIPELINE_ROOT / WORKSPACE_ROOT / CONFIG_DIR
├── requirements.txt
├── .env                 ← local secrets (gitignored)
├── audio/ input/ output/ subtitles/ series/ .cache/   ← legacy runtime dirs
└── *.py                 ← shims → cli/ or lib/ (keep old commands working)
```

## Commands (preferred)

```bash
python3 content_pipeline/cli/process_stream.py --mode transcribe --project my-video
python3 content_pipeline/cli/render_manifest.py --manifest "…" --project my-video --type shorts
python3 content_pipeline/cli/run_module.py --module render --project my-video -- --manifest "…"
python3 content_pipeline/cli/viral_captions.py --help
```

Same via shims:

```bash
python3 content_pipeline/process_stream.py …
python3 content_pipeline/auto-edit.py …   # → cli/auto_edit.py
```

## Rules

| Do | Don’t |
|----|--------|
| Put new **runnable** scripts in `cli/` | Dump new `.py` at the pipeline root |
| Put shared helpers in `lib/` | Import from stage job folders |
| Put JSON knobs in `config/` | Hardcode trigger/censor lists in code |
| Keep `PIPELINE_ROOT` for `audio/`, `.cache/`, `.env` | Assume `__file__.parent` is the pipeline root |

Job footage lives under `step-1-projects/` / `step-2-viral-edit/` — not here.
