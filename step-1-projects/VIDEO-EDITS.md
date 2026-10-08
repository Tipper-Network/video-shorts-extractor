# Video edits — queue

Operator queue for cut work. Session todos mirror this; this file survives restarts.

## Stages

| Step | Folder | What happens |
|------|--------|--------------|
| 1 | `step-1-projects/` | Ingest, plan, script, cut shorts + chunks → `output/deliverables/` |
| 2 | `step-2-viral-edit/` | Viral polish → **`viral/`** (cut stays in `output/`) |
| 3 | `step-3-flywheel-organiser/` | Series / flywheel order |
| 4 | `step-4-ready-to-post/` | Publish-ready pack |

**Handoff rule (1→2):** when a job’s shorts and chunks are done (scripts signed, drafts or approved renders in `output/deliverables/`), **move the whole job folder** from `step-1-projects/{name}/` → `step-2-viral-edit/{name}/`. Do not leave a half-cut job in step 2.

**Empty step-1 rule:** only clear / move jobs out of `step-1-projects/` when that job is ready for viral (scripts approved + cuts). Do not move early. Downstream: step-2 → step-3 when `viral/approved/` is signed — do not park finished viral work forever in step-2.

**Viral folder (step 2):** write captions / on-screen type / covers only under `{name}/viral/{shorts,covers,approved}/`. Never overwrite `output/`. When `viral/approved/` is signed, move the job → `step-3-flywheel-organiser/`. See [`../step-2-viral-edit/README.md`](../step-2-viral-edit/README.md).

## Queue

### The-GAF-program — Future Ready

**Folder:** `step-1-projects/The-GAF-program future ready vids/`  
**Status:** step-1 **cut complete** 2026-10-07 — 30 shorts + 12 chunks rendered. Ready for step-2 when you say move.

| # | Task | Status |
|---|------|--------|
| 1 | Ingest lecture `.srt` → clocks / plains / ebooks | done |
| 2 | `story_snippet` → `output/plan/story_snippets.json` (31) | done |
| 3 | Shorts scripts (30) + chunk scripts (12) | done — approved |
| 4 | Render shorts + chunks (6 lecture manifests) | **done** — all durations in range |
| 5 | **Move job to `step-2-viral-edit/`** for viral | pending — say the word |

Books done. Do not Whisper. Do not overwrite lecture 13 Whisper clocks.
