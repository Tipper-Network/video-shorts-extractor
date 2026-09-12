# The Origin Story — Project Index

**ID:** `origin-story`  
**Requirements:** [`requirements.md`](requirements.md)

## Instruction files (read these — do not regenerate)

| File | Purpose |
|------|---------|
| [`shorts_instructions.md`](shorts_instructions.md) | 5 vertical shorts — timestamps, assembly, overlays |
| [`youtube_instructions.md`](youtube_instructions.md) | 3 mid-form YouTube chapters (11–15 min, 16:9) |

## Persistent artifacts

| File | Purpose |
|------|---------|
| `output/transcript/transcript.txt` | Full timestamped transcript (always after transcribe) |
| `output/plan/manifest.json` | Approved cut list — shorts + chapters |

## Workflow

```
input/0. Origin story.mp4
  → transcribe → output/transcript/transcript.txt
  → plan/manifest.json (5 shorts + 3 chapters)
  → deliverables/youtube/
```

## Commands

```bash
python3 content_pipeline/run_module.py --module transcribe --project origin-story

python3 content_pipeline/render_manifest.py \
  --manifest "projects/0. the origin story/output/plan/manifest.json" \
  --project origin-story
```
