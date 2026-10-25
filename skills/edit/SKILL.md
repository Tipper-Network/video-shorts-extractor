---
name: edit
description: The edit this repo actually runs, from the cut through viral stage 2. Use when rendering or polishing a signed short or chunk. Brand and posting strategies are other organizations.
---

# Edit

Selection has already named the land and the script is signed. This is the picture. Two steps. Do not invent a third polish stage.

```text
step-1  cut
  render_clip_entry     cut_utils.py
    aspect_filter       9:16 blur stack, or 16:9 capped at 1920
    cut_video           one window
    cut_montage         supercut segments, hard joins
    apply_trim          only if the manifest turns trim on
    level_speech        always, VOICE_AF

step-2  viral/          never writes into output/
  stage 1  captions     cli/viral_captions.py
  stage 2  sounds       cli/viral_sounds.py
  approved              human signs, then the job can leave
```

Zoom is not a stage. `cli/viral_zoom.py` exits on purpose. `cli/auto_edit.py` still has a 4-second zoom. Do not run it.

| Syllabus item | Where it lives here |
|---------------|---------------------|
| First 3 seconds | The signed script. `hook-first` puts the punchline first. No separate sting. |
| Open loop | The short still lands. The next stage is a later posting concern. |
| Retention graph | Not in this repo. A bad hold becomes a `_v2` script. |
| Change every 2–4s | Not a rule. The cancelled zoom was that timer. |
| 16:9 → 9:16 | `aspect_filter("9:16")`. Full frame, blurred fill. No face tracker. |
| Precision cut | `cut_video` / `cut_montage` on sentence edges from the script. |
| Silence | `apply_trim`. Chunks: `light` (gap > 2.5s). Shorts: one profile, `moderate` (auto-editor 0.6s), and only when trim is on. |
| Multicam, speed ramp, J-cut, L-cut | No function. One camera. Audio stays on the mouth. |
| Kinetic captions | Step 2 stage 1. ASS, 4 words, active-word color, `margin_v` 500. |
| B-roll, lower thirds, green screen | No function. The lecture is the picture. |
| SFX | Step 2 stage 2. Trigger words, 0.4 volume, 0.8s cooldown. Censor words beep. |
| Voice | `level_speech`. Compressor, dynaudnorm, limiter, loudnorm −16 LUFS, LRA 4. |
| Music bed | No function. Do not add one in the edit. |
| Brand colors and font | `brands/assets/{entity}/caption.json` on the caption burn. |
| Thumbnail | `viral/covers/` is a folder. Nothing generates the frame. |
| CTA card | Not an edit stage. Pack copy is step 4, and posting strategy is later. |

Subcategory files: [`retention`](retention/SKILL.md), [`timeline`](timeline/SKILL.md), [`type`](type/SKILL.md), [`audio`](audio/SKILL.md), [`package`](package/SKILL.md).
