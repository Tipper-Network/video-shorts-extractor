# Local Content Pipeline — Setup

The **product** is this repo: transcribe, plan, render shorts and chunks.

The **UI today** is a local folder + Cursor. The **UI later** is a website talking to the same agents. Do not put job footage or brand books in git.

## 1. Environment

```bash
pip install -r content_pipeline/requirements.txt
```

- **Faster-Whisper** — transcripts
- **Vosk** (optional) — word timestamps (`VOSK_MODEL_PATH`)
- **FFmpeg** — cuts
- **MoviePy** — polish (`--polish`)
- Optional SFX keys: `content_pipeline/.env.example`

## 2. What you copy vs what you keep private

```text
clone/
├── content_pipeline/     # scripts (git)
├── skills/               # cut rules (git)
├── planning/             # playbooks + schemas (git)
├── projects/
│   ├── README.md         # git
│   ├── _template/        # git — copy this
│   └── {your-job}/       # local — gitignored
└── brands/
    ├── README.md         # git
    ├── _template.md      # git — copy this
    └── {entity}.md       # local — gitignored
```

See [`projects/README.md`](projects/README.md).

## 3. Start a job

```bash
cp -r projects/_template projects/my-video
cp brands/_template.md brands/my-entity.md
# Drop source in projects/my-video/input/
# Entity field in requirements.md = file stem of the brand file
```

Paths resolve through `content_pipeline/project_paths.py` from `projects/{name}/`.
