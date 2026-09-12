---
name: reveal-build
description: Short-form style for silent craft/build timelapse — finished result first, then ascending process montage from source clips. Use for carpentry, maker, workshop content.
project: hikmat
style_id: reveal-build
---

# Reveal-Build (short-form style)

**Style ID:** `reveal-build`  
**Also known as:** result-first montage, payoff-first timelapse

## What it is

A vertical short that **opens on the finished piece**, then rewinds through **ascending chronological cuts** from the build sessions, optionally **closing on the result again**.

No narration required. Works for carpentry, furniture, code UI builds, any visual process log.

## Structure

```
REVEAL   0:00–0:05   Best result still (JPG from source folder)
BUILD    0:05–1:00   Process montage — one cut per video clip, ascending (1→11)
RETURN   last 5s     Second result still (loop bait)
```

Clip 11's **build** slice uses mid-session action (~50% offset), not the opening or the money-shot end — that keeps the last build beat as final action before the still return.

## Edit rules

| Rule | Value |
|------|-------|
| `cut_mode` | `supercut` — `segments[]` in manifest |
| Clip order in BUILD | **All 11 video clips**, ascending by `clip_index` |
| REVEAL / RETURN | Result stills from `clip-map.json` → `stills[]` (`type: image`) |
| Platform variants | **Same segments** — only `segment_len_sec` differs (YouTube 5s, TikTok 3.5s) |
| Segment length | 5s (YouTube/Reels), 3.5s (TikTok) |
| Total length | ~65s YouTube (13 × 5s), ~45s TikTok (13 × 3.5s) |
| Trim on render | **off** (silent footage) |
| flywheel | **n/a** — not marketing flywheel content |

## Manifest fields

```json
{
  "short_form_style": "reveal-build",
  "hook_type": "result-first",
  "cut_mode": "supercut",
  "segments": [
    { "type": "image", "path": "~/Desktop/hikmat-project/20260731_121250.jpg", "duration": 5.0, "label": "reveal" },
    { "start": 8.0, "end": 13.0, "label": "build", "clip_index": 1 },
    { "start": 555.8, "end": 560.8, "label": "build", "clip_index": 11 },
    { "type": "image", "path": "~/Desktop/hikmat-project/20260730_115835.jpg", "duration": 5.0, "label": "return" }
  ]
}
```

Segment labels: `reveal` | `build` | `return` (replacing result-hook / process / result-close).

## Pipeline

```bash
python3 content_pipeline/compose_shorts.py --project hikmat
python3 content_pipeline/render_manifest.py \
  --manifest content_pipeline/output/hikmat/manifest.json \
  --project hikmat --no-trim
```

## Platform targets

Same Reveal-Build structure; vary segment density per skill:
- `projects/hikmat/skills/youtube_shorts.md`
- `projects/hikmat/skills/tiktok_shorts.md`
- `projects/hikmat/skills/instagram_reels.md`
