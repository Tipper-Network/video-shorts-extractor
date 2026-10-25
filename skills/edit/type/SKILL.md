---
name: edit-type
description: Step 2 stage 1 kinetic captions. Use when burning brand type onto a cut master. Script is content_pipeline/cli/viral_captions.py.
---

# Type

Step 2, stage 1. Script: `content_pipeline/cli/viral_captions.py`.

Read the cut from `output/deliverables/` (prefer `shorts_approved/`). Write `viral/stage1/{stem}.mp4` plus the `.ass`. Do not write back into `output/`.

## What the burn does

1. Extract 16 kHz mono wav from the cut.
2. Reuse `*_words.json` when it is already next to the cut or the output. Whisper `small` only when that file is missing. If `--script` is passed, a token that disagrees with the script is replaced by the script's word (`gaff` → `GAF` is the same rule). Timestamps stay.
3. Load `brands/assets/{entity}/caption.json` and that entity's font.
4. Build an ASS at 1080×1920. Four words a line. The spoken word is `active`. The land word (the last content words of the script's resolve) is also `active`, bold, and scaled to 118, inside that same line. Stroke from `stroke` / `stroke_width`. Alignment bottom-center. `margin_v` must be **500** or the burn refuses. No second title.
5. Burn with ffmpeg `ass=` filter, `crf` 18, audio copied.

On-screen words are uppercased. `censor_words.json` prints as `****`. `gaff` is rewritten to `GAF` before the burn.

Reburn height in place with `content_pipeline/cli/reburn_caption_margin.py --margin 500`. No `_marginv*` copies.

## What this stage does not do

No stock B-roll, no lower third, no tweet card, no chart, no green screen. Those have no script. The board in the 16:9 frame is the graphic.
