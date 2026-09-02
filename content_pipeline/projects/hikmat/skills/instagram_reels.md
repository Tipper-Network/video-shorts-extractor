---
name: hikmat-instagram-reels
extends: skills/instagram_reels/SKILL.md
project: hikmat
content_type: carpentry-timelapse
---

# Hikmat — Instagram Reels (30–90s)

> Adapted from platform [`instagram_reels`](../../../../skills/instagram_reels/SKILL.md).  
> Strategy: [`content-strategy.md`](../content-strategy.md)

## Content goal

**Aesthetic, self-contained build story** — result hook, then a slightly slower process montage that feels complete. Reels audience saves “how it's made” content.

## Platform constraints

| Field | Value |
|-------|-------|
| Aspect | 9:16 |
| Min duration | 30s |
| Max duration | 90s (prefer 45–75s for this project) |
| Silence trim | **Skip** |
| Brand colors on subs | Optional — match craftsman/shop if known |

## Hook structure (required)

```
0:00–0:05  Result reveal — hold slightly longer than TikTok (let it land)
0:05–1:10  Process montage — 5–8s cuts, ascending order, fewer jumps
1:10–1:15  Clean outro on finished piece
```

Reels can **breathe** — fewer cuts, longer holds on satisfying moments (planing, joinery close-ups).

## Cut rules

1. **5–8s segments** — slower than TikTok
2. **6–10 segments** in 50–70s montage
3. Self-contained arc: problem (raw materials) → process → payoff (finished piece)
4. Lower-third safe zone if adding text — avoid Instagram UI overlap

## Visual

- Clean sans-serif lower-third title on hook: “[Piece name] — start to finish”
- Highlight key craft moments (joint fitting, sanding, final assembly)

## Manifest fields

```json
{
  "target": "instagram",
  "aspect": "9:16",
  "hook_type": "result-first",
  "content_type": "carpentry-timelapse",
  "min_len": 30,
  "max_len": 90,
  "segment_len_sec": 6,
  "flywheel_stage": "n/a"
}
```

## CTA outro (optional)

Simple save/follow prompt — no THP service funnel language.
