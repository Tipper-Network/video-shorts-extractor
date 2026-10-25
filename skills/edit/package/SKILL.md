---
name: edit-package
description: What the edit enforces from the brand, and what it leaves for later. Use when checking caption.json, covers, or a CTA on a cut.
---

# Package

During the edit, the brand shows up in one place: `brands/assets/{entity}/caption.json`, burned in step 2 stage 1. Font file, `body`, `active`, `stroke`, `stroke_width`, `font_size`, `margin_v`. Founder, Tipper, and GAF each have their own file. Do not borrow another entity's font or colors onto this cut.

Spoken brand rules (what the line is allowed to say) are [`entity_brand`](../../entity_brand/SKILL.md). They are applied when the script is written, not in ffmpeg.

## Frame

`viral/covers/` is the folder for a still. No script picks the frame. If a cover is needed, it is the land frame from the signed cut, saved by hand.

## Call to action

No mid-roll card, no end screen, no subscribe pop-up in step 1 or step 2.

The next stage of the wheel is written later, when a job is in step 3 and step 4 (`viewer_state`, `next_stage`, the pack markdown). That is the posting side. It is not an edit stage. [`humaniser`](../../humaniser/SKILL.md) is for that pack copy when it is written.
