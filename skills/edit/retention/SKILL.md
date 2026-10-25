---
name: edit-retention
description: Open and frame of a signed short, as this repo renders them. Use when checking the first line and the 9:16 stack. Step 1 of the edit.
---

# Retention

Step 1, inside the cut. The function is `aspect_filter` in `content_pipeline/lib/cut_utils.py`. The first three seconds are decided earlier, in the signed script.

## First three seconds

`hook-first` plays the punchline, then the setup, then the land. `story-first` opens on the situation. `contiguous` is one window when the take already holds all three.

That opening is his sentence from the tape. Stage 1 captions start with the first word. There is no pre-roll, sting, or zoom in those three seconds.

## Hold

The splice is only the beats in `segments[]`. A new shot is the next beat of the same situation. `cli/viral_zoom.py` is cancelled because a zoom every few seconds was a timer, not a turn. Do not put that timer back with `cli/auto_edit.py`.

YouTube retention is not read. If a cut dies in the middle, change the script and render `_v2`.

## Frame

`cut_video` seeks one second early, then `-ss` after `-i` trims to the script clock. The first frame is the punchline's first phoneme, not the previous keyframe. Stage 1's first cue is that word. There is no second graphic.

`aspect_filter("9:16")`:

- Split the frame.
- Background: scale up, crop to 1080×1920, `boxblur=20:10`. Ungraded.
- Foreground: the whole 16:9 frame at 1080 wide, centered, board included.

`flat: true` on the manifest entry adds one grade on that foreground only: `eq` contrast 1.06, saturation 1.08, and a small warm `colorbalance`. Nothing tracks a face.

Chunks call `aspect_filter("16:9")`: `scale='min(1920,iw)':-2`. 720p stays 720p.

One file. Shorts, Reels, and TikTok do not get their own frame.
