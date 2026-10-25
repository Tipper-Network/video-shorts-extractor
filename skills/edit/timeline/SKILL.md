---
name: edit-timeline
description: How a signed script becomes a timeline in ffmpeg. Use when rendering step 1. Covers cut_video, cut_montage, and apply_trim.
---

# Timeline

Step 1. `render_clip_entry` in `content_pipeline/lib/cut_utils.py`, called from `content_pipeline/cli/render_manifest.py`.

## The cut

| `cut_mode` | Function | What it does |
|------------|----------|----------------|
| `contiguous` | `cut_video` | `-ss` start, `-t` duration, video and audio together. |
| `supercut` | `cut_montage` | One temp mp4 per segment, then concat. Copy concat first. Re-encode only if the streams differ. |

In and out are the script clocks, on sentence edges. A join between segments is a hard cut. There is no J-cut, no L-cut, no second angle, and no speed ramp in this code.

`script_approved: false` skips the short unless `--allow-unapproved`. An existing file is not overwritten. The next pass is `_v2`.

## Silence

`apply_trim` runs only when trim is enabled for that render.

| Level | Method | Used for |
|-------|--------|----------|
| `light` | ffmpeg, drop gaps longer than 2.5s at −40 dB | Chunks (`target` youtube) |
| `moderate` | auto-editor, margin `0.6sec` | Shorts, one profile |
| `aggressive` | auto-editor, margin `0.4sec` | Defined in `trim_profiles.py` for a TikTok target. Do not set it. One file, one short trim. |
| `off` | none | Trim was not turned on |

`trim_profiles.TARGET_DEFAULTS` still maps `tiktok` → `aggressive`. The short renderer passes `clip_target="short"`, which is not in that map, so a short gets the manifest or project trim, not the TikTok preset.

Filler words are not a trim setting. "Sorry", "let's do this", and handwriting are left out of `segments[]` when the script is written.

After the trim, `level_speech` always runs. See [`audio`](../audio/SKILL.md).
