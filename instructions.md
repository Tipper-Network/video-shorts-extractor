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
├── projects/                         # ONE FOLDER PER JOB (input + output + config)
│   ├── README.md
│   ├── _template/                    # Copy to start a new project
│   ├── origin-story/
│   │   ├── input/                    # Drop raw footage here
│   │   ├── output/
│   │   │   ├── transcript/           # transcript.txt + segments.json
│   │   │   ├── plan/                 # manifest.json
│   │   │   ├── deliverables/
│   │   │   │   ├── shorts/           # Vertical (YT, TikTok, Reels)
│   │   │   │   └── chunks/           # 11-15 min mid-form
│   │   │   ├── logs/
│   │   │   └── cache/
│       ├── requirements.md
│       ├── brief.md
│       ├── pipeline.json
│       └── *_instructions.md         # Persistent creative briefs
├── content_pipeline/                 # Shared scripts only (no project data)
│   ├── concat_clips.py
│   ├── compose_shorts.py
│   ├── render_manifest.py
│   └── project_paths.py
├── planning/                         # Playbooks, architecture, schemas
└── skills/                           # Platform-wide editing rules
```

See [`projects/README.md`](projects/README.md).

## 3. Separation from THP

| Concern | Where |
|---------|-------|
| Series themes, observation scripts, brand voice | THP `the-hard-port-os/content/youtube/` |
| Flywheel stage definitions (attract → loop) | THP `THP-MEDIA-001` + [`planning/vision.md`](planning/vision.md) |
| Visual/editorial language (grids, maps, evidence labels) | THP `THP-MEDIA-003` |
| Transcription, cut points, aspect ratios, render | **This workspace** |

Do not merge THP strategy docs into this repo. Link to them; implement the tooling here.

## 4. Starting a project

```bash
cp -r projects/_template projects/my-video
# Drop source files in projects/my-video/input/
# Fill requirements.md, set playbook_id in pipeline.json
```

Scripts resolve paths via `content_pipeline/project_paths.py` from `projects/{name}/`.
