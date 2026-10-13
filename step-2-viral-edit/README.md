# Step 2 — Viral edit

Jobs land here **after** shorts + chunks are cut in [`../step-1-projects/`](../step-1-projects/). The whole job folder moves; do not leave a half-cut job here.

**Stage:** polish signed cuts into social-ready picture. Cut masters stay under `output/`. Viral end results go under **`viral/`** — never overwrite `output/`.

## Stages (current)

| Stage | Does | Script |
|-------|------|--------|
| **1 — Captions** | Kinetic burn-in from brand `caption.json` + tier-A `****` on screen | `content_pipeline/cli/viral_captions.py` |
| **2 — Sounds** | Tier-A mute+beep + word-trigger SFX (`sfx_triggers.json`) | `content_pipeline/cli/viral_sounds.py` |

**Zoom is cancelled** for now (was a blind 1.15× timer). If it returns, it needs a content-aware strategy and likely runs *before* captions — not as a stage between them.

```text
cut shorts_approved/*.mp4
  → viral/stage1/   captions
  → viral/stage2/   sounds
  → viral/approved/ after you sign off
```

Also mirror the latest pass into `viral/shorts/` when handy for A/B.

## Layout (every job)

```text
step-2-viral-edit/{name}/
├── input/
├── output/                     ← CUT ONLY
│   └── deliverables/{shorts,shorts_approved,chunks}/
└── viral/
    ├── stage1/                 ← captions
    ├── stage2/                 ← sounds
    ├── shorts/                 ← optional mirror of latest
    ├── covers/
    └── approved/               → step-3 when signed
```

## Rules

1. **Read** cut masters from `output/deliverables/` (prefer `shorts_approved/`).
2. **Write** only under `viral/`. Same stem as the cut.
3. Never overwrite the cut master. Next pass uses `_v2` inside `viral/` if needed.
4. When `viral/approved/` is signed, move the job → [`../step-3-flywheel-organiser/`](../step-3-flywheel-organiser/).
5. **Caption height:** brand `caption.json` `margin_v` = **500** (all entities). Reburn in place via `content_pipeline/cli/reburn_caption_margin.py` — do not leave `_marginv*` A/B copies.

## Temp / duplicate videos (what to keep when posting)

One ship surface per short. Everything else is disposable after the next stage is signed.

| Keep | Path | Why |
|------|------|-----|
| Cut master | `output/deliverables/shorts_approved/{stem}.mp4` | Source of truth — never delete |
| Ship file | `viral/approved/{stem}.mp4` **or** step-4 pack mp4 | What you post |
| Pack copy | `step-4-ready-to-post/{entity}/{series}/…/{stem}.mp4` | Publish shelf (same bytes as approved after reburn) |

| Trash after sign-off | Path | Why |
|----------------------|------|-----|
| Caption draft | `viral/stage1/{stem}.mp4` | Intermediate; regenerate from cut + ASS |
| Sounds draft | `viral/stage2/{stem}.mp4` | Intermediate once `approved/` is current |
| Mirror / A/B | `viral/shorts/`, `*_v2.mp4`, `*_marginv*.mp4` | Experiments — move to `viral/.trash/` then empty |
| Old ASS experiments | `*_marginv*.ass`, `.trash_margin_tests/` | Not ship |

**Posting checklist**

1. Confirm step-4 (or `viral/approved/`) is the raised-caption + sounds build.
2. Post from **that one file** only.
3. Do not keep parallel `_marginv400` / stage copies “just in case” — cut master + ASS + words.json can rebuild.
4. Optional cleanup after a series is fully posted: `trash viral/stage1/*.mp4 viral/stage2/*.mp4 viral/shorts/` (keep `.ass` + `*_words.json`).

## Template

```bash
mkdir -p "step-2-viral-edit/{name}/viral/"{stage1,stage2,shorts,covers,approved}
```
