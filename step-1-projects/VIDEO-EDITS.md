# Video edits — queue

Operator queue for cut work. Session todos mirror this; this file survives restarts.

## Stages

| Step | Folder | What happens |
|------|--------|--------------|
| 1 | `step-1-projects/` | Ingest, plan, script, cut shorts + chunks → `output/deliverables/` |
| 2 | `step-2-viral-edit/` | Viral polish → **`viral/`** (cut stays in `output/`) |
| 3 | `step-3-flywheel-organiser/` | Series / flywheel order |
| 4 | `step-4-ready-to-post./` | Publish-ready pack |

**Handoff rule (1→2):** when a job’s shorts and chunks are done (scripts signed, drafts or approved renders in `output/deliverables/`), **move the whole job folder** from `step-1-projects/{name}/` → `step-2-viral-edit/{name}/`. Do not leave a half-cut job in step 2.

**Viral folder (step 2):** write captions / on-screen type / covers only under `{name}/viral/{shorts,covers,approved}/`. Never overwrite `output/`. When `viral/approved/` is signed, move the job → `step-3-flywheel-organiser/`. See [`../step-2-viral-edit/README.md`](../step-2-viral-edit/README.md).

## Queue

### Program Future Ready — GAF

**Folder:** `step-1-projects/program future ready vids/`  
**Status:** paused 2026-09-23. Do not process until asked.

| # | Task | Status |
|---|------|--------|
| 1 | Ingest lecture `.srt` files already in `lectures/13–18/` | pending |
| 2 | Mark chunk jobs + short rows to script (`chunk_extraction.md` / `shorts_extraction.md`) | pending |
| 3 | Script → approve → render shorts + chunks | pending |
| 4 | **Move job to `step-2-viral-edit/program future ready vids/`** for viral edit | pending — after 3 |

Books done. Extraction candidates written. Do not Whisper. Do not overwrite lecture 13 Whisper clocks.
