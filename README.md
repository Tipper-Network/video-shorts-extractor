# Content Pipeline

Clone this repo to turn long speech video into **shorts** (9:16) and **chunks** (16:9, 11–15 min), then polish those cuts for social.

This is the **engine**. Jobs, brand books, and memory are not in git. Today you drop files in staged folders; later a website UI will call the same agents and the same `manifest.json` → ffmpeg path.

## Evolution

| Era | What changed |
|-----|----------------|
| **v0** | Single-clip script + local Ollama planner |
| **v1 cut engine** | Cursor agent plans → `manifest.json` → batch FFmpeg. Ollama removed. Deliverables = shorts + chunks only (no platform fan-out) |
| **Operator stages** | Jobs move through folders: cut → viral → flywheel → ready-to-post. Cut masters stay in `output/`; viral finish writes to `viral/` |
| **Speed path** | Sidecar `.srt` skips Whisper; supercut `-c copy`; no 16:9 upscale; shorts `--jobs 4`; `level_speech` on finished files |
| **Next** | Viral polish skills (`captions`, `on-screen-type`, `cover-frame`) writing into `viral/`; website UI later |

```
┌─────────────────────────────────────────────────────────────┐
│  GIT (product)                                              │
│  content_pipeline/  skills/  planning/  *_template/  READMEs│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  LOCAL (operator / future accounts)                         │
│  step-1…4 job folders · brands/ · memory · USER · MEMORY    │
│  ~/.cursor/skills/  (influencer house — not shipped)        │
└─────────────────────────────────────────────────────────────┘
```

## Current flow

```
step-1-projects/          CUT
  input/ → Whisper or .srt → manifest.json → output/deliverables/
        shorts/ + chunks/ (+ shorts_approved/)
        │
        │ move whole job folder
        ▼
step-2-viral-edit/        VIRAL POLISH
  read output/deliverables/  →  write viral/{shorts,covers,approved}/
  (never overwrite output/)
        │
        │ move when viral/approved/ signed
        ▼
step-3-flywheel-organiser/   PUBLISH ORDER (attract → loop)
        │
        ▼
step-4-ready-to-post/        FINAL PACK
```

Queue + handoff rules: [`step-1-projects/VIDEO-EDITS.md`](step-1-projects/VIDEO-EDITS.md).

| Step | Folder | Writes |
|------|--------|--------|
| 1 Cut | [`step-1-projects/`](step-1-projects/) | `output/deliverables/` |
| 2 Viral | [`step-2-viral-edit/`](step-2-viral-edit/) | `viral/{shorts,covers,approved}/` |
| 3 Flywheel | [`step-3-flywheel-organiser/`](step-3-flywheel-organiser/) | order / queue |
| 4 Ready | [`step-4-ready-to-post/`](step-4-ready-to-post/) | publish pack |

**Entity** comes from the video/folder title (Tipper / THP / GAF / founder). Do not mix brands. Brand books live in local [`brands/`](brands/).

## Repo layout

```text
workspace/
├── content_pipeline/     # Whisper, FFmpeg, render, project_paths
├── skills/               # Cut rules (extract, vertical, chunks, entity, …)
├── planning/             # Playbooks, flywheel, schemas, instincts
├── SKILL.md              # Master orchestrator
├── brands/               # Operator brand books (gitignores contents)
├── step-1-projects/      # Cut jobs + VIDEO-EDITS.md queue
├── step-2-viral-edit/    # Jobs after cut; viral/ end results
├── step-3-flywheel-organiser/
├── step-4-ready-to-post/
└── (legacy) projects/    # Scripts still resolve here until retargeted
```

> **Path note:** `content_pipeline/project_paths.py` still looks under `projects/`. Stage folders are the operator UI. Until scripts scan `step-1-projects/` / `step-2-viral-edit/`, point `--project` at a folder the resolver can find, or symlink. Do not invent a second cut language for a future site.

## Onboard (cut)

```bash
pip install -r content_pipeline/requirements.txt

cp -r step-1-projects/_template step-1-projects/my-video
# Drop source in step-1-projects/my-video/input/
# brands/_template.md → brands/{entity}.md
# Set playbook_id in pipeline.json; entity in requirements.md from the title

python3 content_pipeline/process_stream.py --mode transcribe --project my-video
# Prefer sidecar input/captions.srt or {stem}.srt — skips full-file Whisper
# --whisper to force Whisper

python3 content_pipeline/render_manifest.py \
  --manifest "step-1-projects/my-video/output/plan/manifest.json" \
  --project my-video \
  --type shorts --no-trim --jobs 4
# then --type chapters --no-trim

# When shorts + chunks are done:
mv "step-1-projects/my-video" "step-2-viral-edit/my-video"
mkdir -p "step-2-viral-edit/my-video/viral/"{shorts,covers,approved}
```

| You are filling in | Lives in |
|--------------------|----------|
| How to cut | `skills/`, `planning/playbooks.md` |
| This video (cut) | `step-1-projects/{name}/` |
| This video (viral) | `step-2-viral-edit/{name}/viral/` |
| This brand | `brands/{entity}.md` (local) |
| Influencer house prompts | `~/.cursor/skills/` (charsheet, UGC, content-engine, digital-product) |

## Cut rules (shipped)

| Skill | Purpose |
|-------|---------|
| `entity_brand` | Title → Tipper / THP / GAF / founder |
| `situation_resolve` | One situation held until it resolves |
| `extract_shorts` | Hook / setup / resolution + coherence gate |
| `vertical_shorts` | 9:16 export (editorial versions, not platforms) |
| `chunks` | 11–15 min 16:9 mid-form |
| `dynamic_zoom` / `sfx_allocation` | Polish primitives (optional) |
| `lecture_ebook` | GAF lecture plains → field book |

**Shorts:** 50s floor, prefer 55–75s, hard 90s. Script `.md` before ffmpeg. Never overwrite playable files — next pass is `_vN`.

**Viral (planned into `viral/`):** captions + safe zone, on-screen type, cover frames. Cut masters in `output/` stay untouched.

## Stack

| Tool | Role |
|------|------|
| Faster-Whisper | Segment transcripts (`small`, CPU) when no sidecar `.srt` |
| Vosk (optional) | Word-level timestamps for SFX |
| FFmpeg | Cut, 9:16 blur letterbox, speech level |
| MoviePy | Optional polish (SFX + zoom) |

**No Ollama.** Planning is an agent (Cursor today). Scripts only transcribe and render.

## Scripts

| Script | Purpose |
|--------|---------|
| `cli/process_stream.py` | `.srt` or Whisper → `output/transcript/` |
| `cli/render_manifest.py` | Batch render from `manifest.json` |
| `cli/concat_clips.py` | Multi-clip assembly |
| `cli/auto_edit.py` | SFX + zoom (`--polish`) |
| `cli/run_module.py` | Module runner from `pipeline.json` |
| `cli/viral_captions.py` | Kinetic captions → `viral/` |

Layout: [`content_pipeline/README.md`](content_pipeline/README.md) (`cli/` / `lib/` / `config/`). Root `content_pipeline/*.py` files are shims.

## What does not belong in git

Footage, transcripts, manifests, renders, brand books, `USER.md` / `MEMORY.md`, job folders under `step-*` / `projects/`. `.gitignore` already excludes them.

## Key docs

| Topic | File |
|-------|------|
| Agent startup | [`AGENTS.md`](AGENTS.md) |
| Setup | [`instructions.md`](instructions.md) |
| Orchestrator | [`SKILL.md`](SKILL.md) |
| Stages / queue | [`step-1-projects/VIDEO-EDITS.md`](step-1-projects/VIDEO-EDITS.md) |
| Viral folder | [`step-2-viral-edit/README.md`](step-2-viral-edit/README.md) |
| Playbooks | [`planning/playbooks.md`](planning/playbooks.md) |
| Flywheel | [`planning/flywheel-strategies.md`](planning/flywheel-strategies.md) |
| Capabilities | [`planning/capability-matrix.md`](planning/capability-matrix.md) |
