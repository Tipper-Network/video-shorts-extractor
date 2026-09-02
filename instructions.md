# Local Content Pipeline — Setup & Structure

Video editing and content creation workspace. Runs locally in Cursor.

**Strategy and scripts** live in the [THP repo](../The-Hard-Port-stuff/The Hard Port/the-hard-port-os/).  
**This folder** is where we execute: transcribe, plan cuts, apply platform rules, render.

## 1. Environment & Setup Checklist

### Speech Recognition & Polish
- **Faster-Whisper** — segment transcripts
- **Vosk** — word-level timestamps for SFX (`VOSK_MODEL_PATH`)
- **MoviePy** — dynamic zoom + SFX overlay
- **sfx_resolver** — on-demand SFX via API or synthetic fallback

### Optional API Keys
- `FREESOUND_API_KEY` / `PIXABAY_API_KEY` — see `content_pipeline/.env.example`

### Python
```bash
pip install -r content_pipeline/requirements.txt
```

## 2. Directory Structure

```text
~/Desktop/workspace/
├── README.md                         # Human entry point
├── SKILL.md                          # Master orchestrator (agent routing)
├── instructions.md                   # This file — setup & layout
├── content_pipeline/                 # Core pipeline
│   ├── process_stream.py             # transcribe or render modes
│   ├── concat_clips.py               # chronological multi-clip assembly
│   ├── render_manifest.py            # batch render from manifest
│   ├── auto-edit.py                  # SFX + dynamic zoom (MoviePy)
│   ├── sfx_resolver.py               # on-demand SFX (API / synthetic)
│   ├── transcribe.py                 # Whisper + Vosk shared module
│   ├── sfx_triggers.json             # word → SFX mapping
│   ├── .env.example                  # optional API keys
│   ├── input/                        # Drop raw MP4s here
│   ├── audio/                        # Extracted 16kHz WAV
│   ├── subtitles/                    # Transcript JSON
│   ├── output/                       # Rendered clips
│   └── series/                       # Series state JSON (flywheel continuity)
├── planning/                         # Design hub
│   ├── vision.md                     # North star + flywheel stages
│   ├── pipeline-architecture.md      # Plan → review → render
│   ├── roadmap.md                    # Build phases
│   ├── agents/                       # Role docs (planner, renderer, QA)
│   ├── instincts/                    # Editing guardrails
│   ├── schemas/                      # manifest.json + series.json
│   └── templates/                    # Example manifests
└── skills/                           # Platform + pipeline rules
    ├── youtube_chunks/               # 10–30 min 16:9 chapters
    ├── youtube_shorts/               # 30–60s 9:16 teasers
    ├── tiktok_shorts/                # 15–60s fast-paced 9:16
    ├── instagram_reels/              # 30–90s visual story 9:16
    ├── dynamic_zoom/                 # Periodic zoom in/out
    ├── sfx_allocation/               # Word-triggered SFX
    ├── plan_stream/                  # Multi-clip planner (planned)
    ├── render_manifest/              # Batch renderer (planned)
    └── flywheel_series/              # Series continuity (planned)
```

## 3. Separation from THP

| Concern | Where |
|---------|-------|
| Series themes, observation scripts, brand voice | THP `the-hard-port-os/content/youtube/` |
| Flywheel stage definitions (attract → loop) | THP `THP-MEDIA-001` + [`planning/vision.md`](planning/vision.md) |
| Visual/editorial language (grids, maps, evidence labels) | THP `THP-MEDIA-003` |
| Transcription, cut points, aspect ratios, render | **This workspace** |

Do not merge THP strategy docs into this repo. Link to them; implement the tooling here.

## 4. External Input Folders

Project-specific raw footage can live outside `input/`:

```text
~/Desktop/hikmat-project/    # Example: chronological clip collection
```

Copy or symlink into `content_pipeline/input/` before processing, or extend scripts to accept `--source-dir`.
