# Hikmat — Project Skills

Adapted platform rules for **carpentry timelapse** shorts. These override generic `skills/` defaults when planning or rendering hikmat.

## Platform source → project override

| Platform skill (generic) | Hikmat override |
|--------------------------|-----------------|
| — | [`reveal_build.md`](reveal_build.md) — **Reveal-Build style** |
| [`skills/youtube_shorts/`](../../../../skills/youtube_shorts/SKILL.md) | [`youtube_shorts.md`](youtube_shorts.md) |
| [`skills/tiktok_shorts/`](../../../../skills/tiktok_shorts/SKILL.md) | [`tiktok_shorts.md`](tiktok_shorts.md) |
| [`skills/instagram_reels/`](../../../../skills/instagram_reels/SKILL.md) | [`instagram_reels.md`](instagram_reels.md) |
| — | [`montage_compose.md`](montage_compose.md) (hybrid workflow) |

## Do not use for hikmat

- `skills/flywheel_series/` — THP marketing flywheel; not applicable
- Speech hooks, filler removal, silence trim — no meaningful audio

## Agent planning order

1. Read [`../content-strategy.md`](../content-strategy.md)
2. Read [`../clip-map.json`](../clip-map.json)
3. Apply platform override for target (`youtube_shorts.md` / etc.)
4. Apply [`montage_compose.md`](montage_compose.md) for multi-clip cuts
5. Write manifest → `content_pipeline/output/hikmat/manifest.json`
