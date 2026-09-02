---
name: hikmat-montage-compose
project: hikmat
---

# Hikmat — Montage Compose (Hybrid Workflow)

How to build **multi-segment shorts** from the master timeline using ascending clip order and result-first hooks.

## Inputs

| File | Purpose |
|------|---------|
| [`clip-map.json`](../clip-map.json) | Master timeline offsets per source clip |
| [`content-strategy.md`](../content-strategy.md) | Hook rules, segment counts |
| Platform skill | `youtube_shorts.md` / `tiktok_shorts.md` / `instagram_reels.md` |

## Step 1 — Build segment pool

For each clip in `clip-map.json`, compute candidate windows:

```
absolute_start = clip.master_start + (clip.duration × offset)
absolute_end   = absolute_start + segment_len  (default 5s)
```

Respect `max_segments` — short clips get fewer candidates.

Tag each candidate:
- `result-hook` — finished piece frame (usually clip #11 end)
- `process` — mid-build action
- `materials` — early/raw state (clips #1–#3)

**Human review required** — shift timestamps ±2s to avoid dead frames.

Output: `content_pipeline/output/hikmat/segment-pool.json`

## Step 2 — Compose montage recipes

Generate 10–15 draft shorts. Each recipe:

1. Pick **1 result-hook segment** (opens the short)
2. Pick **5–11 process segments** from ascending clips
3. Optionally **close with result** (same or different angle)
4. Sum durations → target per platform skill

**Ordering rule:** sort selected segments by `master_start` ascending. Exception: hook segment plays first even if chronologically last (result-first).

### Example recipe

| Order in edit | Clip | Master time | Label |
|---------------|------|-------------|-------|
| 1 (hook) | #11 | 580–585s | result-hook |
| 2 | #1 | 8–13s | materials |
| 3 | #4 | 160–165s | process |
| 4 | #5 | 270–275s | process |
| 5 | #7 | 420–425s | process |
| 6 | #10 | 485–490s | process |
| 7 (outro) | #11 | 600–605s | result-close |

Total: ~35s → valid YT Short + TikTok

## Step 3 — Single-clip shorts (hybrid)

For clips #5 (159s) and #11 (109s), also draft **one continuous window**:

```json
{
  "id": "sh_single_01",
  "title": "Session highlight — long build clip",
  "hook_type": "result-first",
  "start": 550.0,
  "end": 595.0,
  "segments": null
}
```

Use when one clip tells a complete mini-story without montage.

## Step 4 — Write manifest

Use [`manifest.template.json`](../manifest.template.json) as starting point.

Required hikmat fields on every short:
- `hook_type`: `"result-first"`
- `content_type`: `"carpentry-timelapse"`
- `flywheel_stage`: `"n/a"`
- `parent_chapter`: `"n/a"`

Montage shorts use `segments[]`:

```json
"segments": [
  { "start": 580.0, "end": 585.0, "label": "result-hook", "clip_index": 11 },
  { "start": 8.0, "end": 13.0, "label": "process", "clip_index": 1 }
]
```

## Step 5 — Render

```bash
python3 content_pipeline/compose_shorts.py
python3 content_pipeline/render_manifest.py \
  --manifest content_pipeline/output/hikmat/manifest.json

# Single short preview
python3 content_pipeline/render_manifest.py \
  --manifest content_pipeline/output/hikmat/manifest.json --only sh01
```

`render_manifest.py` supports `segments[]` montages — cuts each segment, concat-crops to 9:16.

## Variant generation tips

- **Variety:** rotate which clips appear — not every montage needs all 11
- **Density variants:** same segment pool → TikTok-tight (3s) vs Reels-slow (7s) versions
- **Naming:** `montage_yt_01`, `montage_tt_01`, `montage_ig_01` from same base recipe

## Quality checklist

- [ ] Opens on clearest finished-piece frame
- [ ] No segment is mostly static/frozen
- [ ] Ascending build logic readable without narration
- [ ] Total length within platform min/max
- [ ] 9:16 crop keeps workpiece centered (portrait sources #4, #10)
