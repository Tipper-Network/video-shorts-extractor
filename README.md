# Content Pipeline

Clone this repo to cut **shorts** (9:16) and **chunks** (16:9, 11–15 min) from long speech video.

This is the **engine**. Jobs, brand books, and memory are not in git. Today you drop files in a folder; later a website UI will call the same agents.

```
Upload / drop footage
        ↓
Whisper transcript
        ↓
Agent plan  →  manifest.json  (shorts + chunks)
        ↓
FFmpeg render
```

**No Ollama.** Planning is an agent (Cursor today, site-connected agents later). Scripts only transcribe and render.

## Onboard

```bash
pip install -r content_pipeline/requirements.txt

cp -r projects/_template projects/my-video
# Drop source in projects/my-video/input/
# Copy brands/_template.md → brands/{entity}.md and fill it
# Set playbook_id in projects/my-video/pipeline.json
# Fill projects/my-video/requirements.md (entity from the video title)

python3 content_pipeline/run_module.py --module transcribe --project my-video
python3 content_pipeline/render_manifest.py \
  --manifest "projects/my-video/output/plan/manifest.json" \
  --project my-video \
  --type shorts --no-trim
```

| You are filling in | Lives in |
|--------------------|----------|
| How to cut | `skills/`, `planning/playbooks.md` |
| This video | `projects/{name}/` (local) |
| This brand | `brands/{entity}.md` (local) |

See [`projects/README.md`](projects/README.md) and [`brands/README.md`](brands/README.md).

## Stack

| Tool | Role |
|------|------|
| Faster-Whisper | Segment transcripts |
| Vosk (optional) | Word-level timestamps |
| FFmpeg | Cut, 9:16 reframe, speech level |
| MoviePy | Polish (SFX + zoom) — captions not shipped yet |

## Scripts

| Script | Purpose |
|--------|---------|
| `run_module.py --module transcribe` | Whisper → `output/transcript/` |
| `render_manifest.py` | Batch render from `manifest.json` |
| `concat_clips.py` | Multi-clip assembly |
| `auto-edit.py` | SFX + zoom (`--polish`) |

## What does not belong in git

Footage, transcripts, manifests, renders, your brand books, `USER.md` / `MEMORY.md`. Those are operator (or future account) data. `.gitignore` already excludes them; untrack anything already committed.
