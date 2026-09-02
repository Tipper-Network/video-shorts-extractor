# Projects — Per-Job Requirements

Each editing project gets its own folder here. **Project requirements stay here.** Reusable editing logic lives in `skills/`, **playbooks**, and `content_pipeline/*.py`.

**Architecture visuals:** [`planning/playbooks.md`](../planning/playbooks.md)  
**Playbook catalog:** [`planning/playbooks/`](../planning/playbooks/)

## Layers

```
PRIMITIVES (ffmpeg, Whisper)
    ↓
MODULES (transcribe, render, …)     ← content_pipeline/modules/README.md
    ↓
PLAYBOOKS (reusable recipes)        ← planning/playbooks/*.json
    ↓
PROJECT (one job)                   ← projects/{name}/
```

| Layer | Question it answers |
|-------|---------------------|
| **Platform** | *How* do we edit? (modules, skills, schemas) |
| **Playbook** | *Which* modules + skills for this **type** of production? |
| **Project** | *What* does **this** video need? (assets, overrides, cuts) |

## Folder layout

```text
projects/
├── README.md                 ← this file
├── _template/
│   ├── requirements.md
│   └── pipeline.json           ← playbook_id + overrides
└── hikmat/
    ├── brief.md
    ├── requirements.md
    ├── pipeline.json           ← playbook_id: timelapse-montage
    ├── content-strategy.md
    ├── clip-map.json         ← master timeline offsets per source clip
    ├── manifest.template.json
    └── skills/               ← platform skill overrides for this project
        ├── README.md
        ├── youtube_shorts.md
        ├── tiktok_shorts.md
        ├── instagram_reels.md
        └── montage_compose.md
```

When a project needs different rules from platform skills (e.g. timelapse vs talking-head), add **`projects/{name}/skills/`** overrides. Agent reads project skills **instead of** generic `skills/` for that job.

## Starting a new project

```bash
mkdir -p content_pipeline/projects/my-project
cp content_pipeline/projects/_template/requirements.md \
   content_pipeline/projects/my-project/requirements.md
cp content_pipeline/projects/_template/pipeline.json \
   content_pipeline/projects/my-project/pipeline.json
# Set playbook_id in pipeline.json — see planning/playbooks/
```

Then fill in:
1. Source folder path
2. Assembly rules (order, exclusions)
3. Story + audience
4. Known issues
5. Desired outputs

Create series state if multi-episode:

```bash
cp content_pipeline/series/README.md  # see series schema
# edit content_pipeline/series/my-project.json
```

## Workflow per project

```
1. Write requirements.md          ← you: what this video needs
2. Run platform scripts           ← concat, transcribe, render
3. Track stages                   ← projects/{name}/pipeline.log.json
4. Agent reads requirements + skills ← planning cuts
5. Output → content_pipeline/output/{name}/
6. Log learnings                  ← update planning/capability-matrix.md
```

### Stage log + timing

Every run writes to:

| File | Contents |
|------|----------|
| `projects/{name}/pipeline.log.json` | Stage history + **duration per step** + running totals |
| `projects/{name}/pipeline.timing.log` | Plain text — easy to `tail -f` |

```bash
# View status + how long each stage took
python3 content_pipeline/pipeline_log.py --project hikmat --show

# Watch live
tail -f content_pipeline/projects/hikmat/pipeline.timing.log
```

Example timing log:
```
2026-09-02 02:10:00  concat         START    mode=full, clips=11
2026-09-02 02:28:45  concat         DONE     (18m 45s)  mode=full, clips=11  → output/hikmat/...
```

Scripts accept `--project hikmat` — they log start, end, and elapsed time automatically.

## What belongs where

| Goes in project `requirements.md` | Goes in platform (skills/code) |
|-----------------------------------|--------------------------------|
| Clip list and sort order | How concat handles portrait/no-audio |
| "Remove 10s pauses on clip 11" | Silence-trim skill + script flags |
| Story intent, audience | Platform pacing rules (TikTok vs YouTube) |
| Photos placement for *this* job | Generic still→video conversion |
| Clips to exclude | Normalization filters |
| Hook strategy, content type | Generic flywheel / THP patterns |
| Project skill overrides (`projects/{name}/skills/`) | Base platform skills (`skills/`) |

## Active projects

| Project | Requirements | Raw assets | Edit base |
|---------|--------------|------------|-----------|
| [hikmat](hikmat/brief.md) | [requirements.md](hikmat/requirements.md) | `~/Desktop/hikmat-project/` | `output/hikmat/hikmat_timeline_normalized.mp4` |

## Capability testing

Each project is an integration test for the platform. Track results in [`planning/capability-matrix.md`](../planning/capability-matrix.md).

After a session: if something broke or was missing → fix platform code/skill → mark matrix → next project benefits.
