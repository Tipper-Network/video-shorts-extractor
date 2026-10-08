# Step 1 — Projects (cut)

Each job is **self-contained and local**. Git only ships `_template/`, this README, and [`VIDEO-EDITS.md`](VIDEO-EDITS.md). Real jobs are gitignored.

**Stage:** cut shorts + chunks here. When both are done, **move the whole job folder** to [`../step-2-viral-edit/`](../step-2-viral-edit/) for the viral-edit pass. Viral polish writes to **`viral/`**, never into `output/`.

Product overview + evolution: [`../README.md`](../README.md). Queue: [`VIDEO-EDITS.md`](VIDEO-EDITS.md).

1. `cp -r step-1-projects/_template step-1-projects/{name}/`
2. Drop raw media in **`input/`** (or per-lecture folders when the job uses that layout)
3. Fill **`requirements.md`** (entity from the video title)
4. Run pipeline scripts with `--project {name}`
5. Collect **cut** files from **`output/deliverables/`**
   - `shorts/` (9:16 — one file per editorial version)
   - `shorts_approved/` (signed-off cut scripts / mp4s)
   - `chunks/` (11-15 min mid-form)
6. **Handoff:** `mv step-1-projects/{name} step-2-viral-edit/{name}` then ensure `viral/{shorts,covers,approved}/` exists

Platform code stays in `content_pipeline/`. Planning stays in `planning/`. **Everything for this job lives here — not in git.**

## Instruction files (persistent briefs)

Save Gemini/agent creative briefs as files — **never regenerate in chat**:

| Pattern | Purpose |
|---------|---------|
| `shorts_instructions.md` / `shorts_extraction.md` | Shorts themes, clocks, scripts |
| `chunk_instructions.md` / `chunk_extraction.md` | Mid-form chunk jobs |
| `requirements.md` | Index + project rules |

Manifest (`output/plan/manifest.json`) holds machine-cut timestamps; instruction files hold creative intent.

## Layout (every project)

```text
step-1-projects/{name}/
├── input/                  ← YOU: raw clips, stills, source video (+ optional .srt)
├── output/
│   ├── transcript/         ← transcript.txt + segments.json
│   ├── plan/               ← manifest.json (edit plan)
│   ├── logs/
│   └── deliverables/       ← CUT masters only
│       ├── shorts/         ← vertical 9:16 drafts
│       ├── shorts_approved/← signed cut scripts / mp4s
│       └── chunks/         ← horizontal 16:9 (11-15 min)
├── *_instructions.md       ← persistent creative briefs
├── requirements.md
├── pipeline.json
└── brief.md                ← agent read-me-first
```

After handoff to step-2, the same tree gains **`viral/`** (see [`../step-2-viral-edit/README.md`](../step-2-viral-edit/README.md)).

## Start a new project

```bash
cp -r step-1-projects/_template step-1-projects/my-video
# Edit requirements.md + pipeline.json (set playbook_id)
# Drop source files in step-1-projects/my-video/input/
```

## Commands

```bash
python3 content_pipeline/process_stream.py --mode transcribe --project my-video
# several videos in input/: one file at a time
python3 content_pipeline/process_stream.py --mode transcribe --project my-video --input "clip.mp4"

python3 content_pipeline/render_manifest.py \
  --manifest "step-1-projects/my-video/output/plan/manifest.json" \
  --project my-video \
  --type shorts --no-trim --jobs 4

python3 content_pipeline/pipeline_log.py --project my-video --show
```

> Scripts still resolve folders under `projects/` by default. Prefer matching folder names, or see root [`README.md`](../README.md) path note.

## What goes where

| In this folder | In platform (`content_pipeline/`, `skills/`) |
|----------------|---------------------------------------------|
| Raw assets, requirements, clip-map | ffmpeg scripts, Whisper, schemas |
| Project skill overrides | Generic platform skills |
| Manifest + cut deliverables | Playbooks, module code |
| (after move) `viral/` end results | Planned captions / type / cover skills |
