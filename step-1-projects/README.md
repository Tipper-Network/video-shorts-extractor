# Step 1 — Projects (cut)

Each job is **self-contained and local**. Git only ships `_template/` and this README. Real jobs are gitignored.

**Stage:** cut shorts + chunks here. When both are done, **move the whole job folder** to [`../step-2-viral-edit/`](../step-2-viral-edit/) for the viral-edit pass. Queue: [`VIDEO-EDITS.md`](VIDEO-EDITS.md).

1. `cp -r step-1-projects/_template step-1-projects/{name}/`
2. Drop raw media in **`input/`** (or per-lecture folders when the job uses that layout)
3. Fill **`requirements.md`** (entity from the video title)
4. Run pipeline scripts with `--project {name}`
5. Collect **cut** files from **`output/deliverables/`**
   - `shorts/` (9:16 — one file per editorial version)
   - `chunks/` (11-15 min mid-form)
6. **Handoff:** move `{name}/` → `step-2-viral-edit/{name}/` — viral polish writes to **`viral/`**, not `output/`

Platform code stays in `content_pipeline/`. Planning stays in `planning/`. **Everything for this job lives here — not in git.**

## Instruction files (persistent briefs)

Save Gemini/agent creative briefs as files — **never regenerate in chat**:

| Pattern | Purpose |
|---------|---------|
| `shorts_instructions.md` | Shorts timestamps, hooks, assembly |
| `chunk_instructions.md` | Mid-form chunks (11-15 min) |
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
│       ├── shorts/         ← vertical 9:16 (platform in filename)
│       └── chunks/         ← horizontal 16:9 (11-15 min)
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
python3 content_pipeline/run_module.py --module transcribe --project my-video
# several videos in input/: one file at a time
python3 content_pipeline/process_stream.py --mode transcribe --project my-video --input "clip.mp4"

python3 content_pipeline/render_manifest.py \
  --manifest "projects/my-video/output/plan/manifest.json" \
  --project my-video \
  --type shorts --no-trim

python3 content_pipeline/pipeline_log.py --project my-video --show
```

## What goes where

| In this folder | In platform (`content_pipeline/`, `skills/`) |
|----------------|---------------------------------------------|
| Raw assets, requirements, clip-map | ffmpeg scripts, Whisper, schemas |
| Project skill overrides | Generic platform skills |
| Manifest + deliverables | Playbooks, module code |
