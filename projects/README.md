# Projects — one folder per job

Each project is **self-contained**. Your workflow:

1. Create or open `projects/{name}/`
2. Drop raw media in **`input/`**
3. Fill **`requirements.md`** with us (story, audience, cuts)
4. Run pipeline scripts with `--project {name}`
5. Collect publish-ready files from **`output/deliverables/`**

Platform code stays in `content_pipeline/`. Planning stays in `planning/`. **Everything for this job lives here.**

## Instruction files (persistent briefs)

Save Gemini/agent creative briefs as files — **never regenerate in chat**:

| Pattern | Purpose |
|---------|---------|
| `shorts_instructions.md` | Shorts timestamps, hooks, assembly |
| `youtube_instructions.md` | YouTube chapter extractions |
| `requirements.md` | Index + links to all instruction files |

Manifest (`output/plan/manifest.json`) holds machine-cut timestamps; instruction files hold creative intent.

## Layout (every project)

```text
projects/{name}/
├── input/                  ← YOU: raw clips, stills, source video
├── output/
│   ├── transcript/         ← transcript.txt + segments.json (always on transcribe)
│   ├── plan/               ← manifest.json (edit plan)
│   ├── logs/
│   └── deliverables/       ← publish-ready exports
│       ├── youtube/
│       ├── tiktok/
│       └── reels/
├── *_instructions.md       ← persistent creative briefs (your Gemini exports)
├── requirements.md         ← index + project rules
├── pipeline.json
├── brief.md                ← agent read-me-first
```

## Start a new project

```bash
cp -r projects/_template projects/my-video
# Edit projects/my-video/requirements.md + pipeline.json (set playbook_id)
# Drop source files in projects/my-video/input/
```

## Commands

```bash
# Transcribe
python3 content_pipeline/run_module.py --module transcribe --project origin-story

# Render deliverables
python3 content_pipeline/render_manifest.py \
  --manifest "projects/0. the origin story/output/plan/manifest.json" \
  --project origin-story

# Pipeline status
python3 content_pipeline/pipeline_log.py --project origin-story --show
```

## Active projects

| Project | Type | Status |
|---------|------|--------|
| [0. the origin story](0.%20the%20origin%20story/brief.md) | Speech flywheel | Transcript done → manifest validation → render |

## What goes where

| In this folder | In platform (`content_pipeline/`, `skills/`) |
|----------------|---------------------------------------------|
| Raw assets, requirements, clip-map | ffmpeg scripts, Whisper, schemas |
| Project skill overrides | Generic platform skills |
| Manifest + deliverables | Playbooks, module code |
