# Hikmat — Project Index

**Requirements:** [`requirements.md`](requirements.md)  
**Pipeline modules:** [`pipeline.json`](pipeline.json)  
**Content strategy:** [`content-strategy.md`](content-strategy.md)  
**Clip timeline:** [`clip-map.json`](clip-map.json)  
**Project skills:** [`skills/README.md`](skills/README.md)

## What this is

Carpentry timelapse — **result-first hook**, process montage, under 60s. No flywheel tagging.

## Workflow

```
11 clips  →  ONE master  →  segment pool  →  montage variants  →  pick winners  →  render 9:16
   ✓            ✓              next              next                 you            pending
```

## Master timeline (Phase 1 — done)

| | |
|---|---|
| File | `content_pipeline/output/hikmat/hikmat_timeline_normalized.mp4` |
| Duration | ~610s (~10 min) |
| Clips | 11 videos, chronological, normalized |

## Phase 2 — shorts (in progress)

Hybrid approach — **segment pool + manifest done**, rendering drafts:

| Artifact | Path |
|----------|------|
| Segment pool | `output/hikmat/segment-pool.json` (28 candidates) |
| Manifest | `output/hikmat/manifest.json` (11 shorts) |
| Renders | `output/hikmat/shorts/` |

```bash
# Regenerate pool + manifest
python3 content_pipeline/compose_shorts.py

# Render all (or one)
python3 content_pipeline/render_manifest.py --manifest content_pipeline/output/hikmat/manifest.json
python3 content_pipeline/render_manifest.py --manifest content_pipeline/output/hikmat/manifest.json --only sh01
```

## Project folder layout

```
projects/hikmat/
├── brief.md                 ← this file
├── requirements.md          ← edit rules, clip list
├── content-strategy.md      ← hook + hybrid workflow
├── clip-map.json            ← master timeline offsets
├── manifest.template.json   ← draft manifest starter
├── skills/                  ← platform skill overrides
├── pipeline.log.json
└── pipeline.timing.log
```
