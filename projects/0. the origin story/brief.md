# The Origin Story — Project Index

**ID:** `origin-story`  
**Requirements:** [`requirements.md`](requirements.md)

## Instruction files (read these — do not regenerate)

| File | Purpose |
|------|---------|
| [`shorts_instructions.md`](shorts_instructions.md) | 5 vertical short concepts — timestamps, assembly, overlays |
| [`chunk_instructions.md`](chunk_instructions.md) | 3 mid-form chapter concepts (batch 1: first 2) |

## Deliverables (batch 1)

| Type | Count | Skill |
|------|-------|-------|
| Shorts (9:16) | 5 concepts, up to 3 editorial versions each | `skills/extract_shorts` + `skills/vertical_shorts` |
| Mid-form chunks 16:9 (11–15 min) | 2 | `skills/chunks` |

## Persistent artifacts

| File | Purpose |
|------|---------|
| `output/transcript/transcript.txt` | Full timestamped transcript (always after transcribe) |
| `output/plan/manifest.json` | Approved cut list — shorts + chapters |

## Workflow

```
input/0. Origin story.mp4
  → transcribe → output/transcript/transcript.txt
  → plan/manifest.json (5 shorts + 2 chunks)
  → deliverables/shorts/*.md (script) → approve → render
  → deliverables/shorts/*.mp4 (drafts)
  → deliverables/shorts_approved/ (signed-off)
  → deliverables/chunks/
```

## Commands

```bash
python3 content_pipeline/run_module.py --module transcribe --project origin-story

python3 content_pipeline/render_manifest.py \
  --manifest "projects/0. the origin story/output/plan/manifest.json" \
  --project origin-story
```
