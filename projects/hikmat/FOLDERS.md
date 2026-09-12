# Hikmat — folder map

Everything for this project lives under **`projects/hikmat/`**.

## Your job

| Step | You do |
|------|--------|
| 1 | Drop clips + stills in **`input/`** |
| 2 | Review/update **`requirements.md`** with agent |
| 3 | Watch **`output/deliverables/`** when render completes |

## Paths

| What | Path |
|------|------|
| Raw input | `projects/hikmat/input/` |
| Master timeline | `projects/hikmat/output/master/timeline_normalized.mp4` |
| Edit plan | `projects/hikmat/output/plan/manifest.json` |
| Publish-ready | `projects/hikmat/output/deliverables/{youtube,tiktok,reels}/` |
| Config | `projects/hikmat/pipeline.json`, `clip-map.json` |
| Stage logs | `projects/hikmat/pipeline.timing.log` |

## Commands

```bash
python3 content_pipeline/compose_shorts.py --project hikmat

python3 content_pipeline/render_manifest.py \
  --manifest projects/hikmat/output/plan/manifest.json \
  --project hikmat --no-trim
```
