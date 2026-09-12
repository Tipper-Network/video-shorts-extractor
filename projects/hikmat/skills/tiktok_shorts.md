---
name: hikmat-tiktok-shorts
extends: skills/tiktok_shorts/SKILL.md
project: hikmat
content_type: carpentry-timelapse
---

# Hikmat — TikTok Shorts (15–60s)

> Adapted from platform [`tiktok_shorts`](../../../../skills/tiktok_shorts/SKILL.md).  
> Strategy: [`content-strategy.md`](../content-strategy.md)

## Content goal

**Instant visual hook + dense process cuts.** TikTok rewards fast pacing and loop-friendly endings. Carpentry timelapse = satisfying transformation without needing speech.

## Platform constraints

| Field | Value |
|-------|-------|
| Aspect | 9:16 (center crop on work) |
| Min duration | 15s |
| Max duration | 60s |
| Silence trim | **Skip** |
| Filler removal | **N/A** |
| Subtitles | Optional — text overlay on hook only (“Watch this table come together”) |

## Hook structure (required)

```
0:00–0:02  Result flash — finished piece, no intro padding
0:02–0:50  Rapid process montage — 3–4s cuts, ascending order
0:50–0:58  Snap back to result (loop bait)
```

TikTok variant is **tighter** than YouTube: shorter segments, more cuts, faster rhythm.

## Cut rules

1. **3–4s segments** preferred (vs 5–6s for Reels)
2. **8–15 segments** in 45–55s montage
3. **Strongest result frame first** — no slow build-up
4. End on result identical or near-identical to opening → encourages replay

## Visual

- Bold text on hook frame only (optional)
- Face tracking: N/A unless craftsman visible — crop to **hands + workpiece**
- Yellow/white keyphrase highlight if using text

## Manifest fields

```json
{
  "target": "tiktok",
  "aspect": "9:16",
  "hook_type": "result-first",
  "content_type": "carpentry-timelapse",
  "min_len": 15,
  "max_len": 60,
  "segment_len_sec": 3.5,
  "flywheel_stage": "n/a"
}
```

## What we drop from platform skill

- Aggressive auto-editor silence trim
- Speech-based instant hook (0:00–0:03 controversial statement)
- `--auto-editor-tightness aggressive` — not useful on silent footage
