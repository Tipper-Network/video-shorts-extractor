# Content Pipeline Workspace

Local-first video editing and content creation — separate from product repos.

## Architecture (v1)

```
Raw footage
    ↓
Whisper / Vosk (local)     → transcript + word timestamps
    ↓
Cursor agent (you + me)    → storyline, manifest.json
    ↓
FFmpeg / MoviePy           → cut, concat, zoom, SFX
    ↓
Platform-ready output
```

**No Ollama.** Planning is interactive in Cursor. Scripts handle mechanical work only.

## What this is vs THP

| Layer | Location |
|-------|----------|
| Strategy — scripts, brand, flywheel intent | THP `the-hard-port-os/` |
| Execution — transcribe, cut, render, SFX | **This workspace** |
| Per-project requirements | `content_pipeline/projects/{name}/` |

## Projects vs platform

| | Platform | Project (e.g. hikmat) |
|---|----------|------------------------|
| **Question** | *How* do we edit? | *What* does this video need? |
| **Lives in** | `skills/`, `content_pipeline/*.py` | `projects/hikmat/requirements.md` |
| **Tested via** | [`planning/capability-matrix.md`](planning/capability-matrix.md) | Each new project folder |

See [`content_pipeline/projects/README.md`](content_pipeline/projects/README.md).

## Stack

| Tool | Role |
|------|------|
| Faster-Whisper | Segment transcripts |
| Vosk | Word-level timestamps (SFX triggers) |
| FFmpeg / auto-editor | Cut, concat, silence trim |
| MoviePy | Dynamic zoom + SFX overlay |
| sfx_resolver | On-demand SFX (API or synthetic) |

## Scripts

| Script | Purpose |
|--------|---------|
| `process_stream.py` | `--mode transcribe` or `--mode render` |
| `concat_clips.py` | Chronological multi-clip assembly |
| `render_manifest.py` | Batch render from manifest.json |
| `auto-edit.py` | SFX + dynamic zoom polish |
| `sfx_resolver.py` | Fetch/generate SFX on demand |

## Quick start

```bash
pip install -r content_pipeline/requirements.txt

# Concat a clip folder (e.g. hikmat)
python3 content_pipeline/concat_clips.py \
  --source-dir ~/Desktop/hikmat-project \
  --series hikmat

# Transcribe
python3 content_pipeline/process_stream.py \
  --mode transcribe --input hikmat/hikmat_timeline.mp4 --vosk

# Render from agent-written manifest
python3 content_pipeline/render_manifest.py \
  --manifest content_pipeline/output/my_stream/manifest.json
```

## Optional env vars

Copy `content_pipeline/.env.example` — Freesound/Pixabay keys improve SFX quality; synthetic fallback works without keys.

## Active projects

- **hikmat** — [`projects/hikmat/requirements.md`](content_pipeline/projects/hikmat/requirements.md) · raw: `~/Desktop/hikmat-project/`
