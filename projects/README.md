# Projects — one folder per job

Each project is **self-contained**. Your workflow:

1. Create or open `projects/{name}/`
2. Drop raw media in **`input/`**
3. Fill **`requirements.md`** with us (story, audience, cuts)
4. Run pipeline scripts with `--project {name}`
5. Collect publish-ready files from **`output/deliverables/`**

Platform code stays in `content_pipeline/`. Planning stays in `planning/`. **Everything for this job lives here.**

## Layout (every project)

```text
projects/{name}/
├── input/                  ← YOU: raw clips, stills, source video
├── output/
│   ├── master/             ← assembled timeline
│   ├── cache/              ← concat intermediates
│   ├── plan/               ← manifest.json (edit plan)
│   ├── logs/               ← run logs
│   └── deliverables/       ← publish-ready exports
│       ├── youtube/
│       ├── tiktok/
│       └── reels/
├── requirements.md         ← project edit rules (you + agent)
├── pipeline.json           ← playbook + module overrides
├── clip-map.json           ← timeline offsets (timelapse projects)
├── brief.md                ← quick index
├── skills/                 ← skill overrides for this job
├── pipeline.timing.log     ← stage timing
└── series.json             ← optional flywheel continuity
```

## Start a new project

```bash
cp -r projects/_template projects/my-video
# Edit projects/my-video/requirements.md + pipeline.json (set playbook_id)
# Drop source files in projects/my-video/input/
```

## Commands

```bash
# Compose edit plan
python3 content_pipeline/compose_shorts.py --project hikmat

# Render deliverables
python3 content_pipeline/render_manifest.py \
  --manifest projects/hikmat/output/plan/manifest.json \
  --project hikmat --no-trim

# Pipeline status
python3 content_pipeline/pipeline_log.py --project hikmat --show
```

## Active projects

| Project | Type | Status |
|---------|------|--------|
| [hikmat](hikmat/brief.md) | Carpentry timelapse | Phase 2 deliverables rendered |

## What goes where

| In this folder | In platform (`content_pipeline/`, `skills/`) |
|----------------|---------------------------------------------|
| Raw assets, requirements, clip-map | ffmpeg scripts, Whisper, schemas |
| Project skill overrides | Generic platform skills |
| Manifest + deliverables | Playbooks, module code |
