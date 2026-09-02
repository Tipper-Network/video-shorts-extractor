---
name: hikmat-youtube-shorts
extends: skills/youtube_shorts/SKILL.md
project: hikmat
content_type: carpentry-timelapse
---

# Hikmat — YouTube Shorts (30–60s)

> Adapted from platform [`youtube_shorts`](../../../../skills/youtube_shorts/SKILL.md).  
> Strategy: [`content-strategy.md`](../content-strategy.md)

## Content goal

**Result-first timelapse teaser** — finished carpentry piece in the first 3 seconds, then fast process montage. Drives curiosity (“how did he make that?”) without narration.

## Platform constraints

| Field | Value |
|-------|-------|
| Aspect | 9:16 |
| Min duration | 30s |
| Max duration | **60s (hard cap)** |
| Silence trim | **Skip** — silent screen recordings |
| Speech hooks | **Skip** — visual hook only |

## Hook structure (required)

```
0:00–0:03  Finished piece — clearest angle, full reveal
0:03–0:55  Process montage — ascending clip order, 4–6s cuts
0:55–1:00  Return to result OR before/after flash
```

## Cut rules

1. **Ascending timeline** — earlier sessions before later ones
2. **6–12 segments** per short at 4–6s each
3. **No dead frames** — skip static UI, loading, held frames
4. **Portrait clips (#4, #10)** — crop center on work/hands; verify 9:16 crop doesn't cut the piece

## Title / overlay (optional pass 2)

- Short descriptive title: “Building a [piece] in 60 seconds”
- No THP flywheel CTA — optional “Full timelapse on channel”

## Manifest fields

```json
{
  "target": "yt-shorts",
  "aspect": "9:16",
  "hook_type": "result-first",
  "content_type": "carpentry-timelapse",
  "min_len": 30,
  "max_len": 60,
  "flywheel_stage": "n/a"
}
```

## Render

```bash
python3 content_pipeline/render_manifest.py \
  --manifest content_pipeline/output/hikmat/manifest.json
```

(Multi-segment montages require `segments[]` support — see `montage_compose.md`.)
