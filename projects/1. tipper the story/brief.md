# Tipper The Story — Project Index

**ID:** `tipper-the-story`  
**Requirements:** [`requirements.md`](requirements.md)

## Instruction files

| File | When to add |
|------|-------------|
| [`shorts_extraction.md`](shorts_extraction.md) | **Planner extraction** — transcript-backed short scripts (use this) |
| [`shorts_instructions.md`](shorts_instructions.md) | Gemini 10-pack (kept for contrast; do not cut from it) |
| [`chunk_instructions.md`](chunk_instructions.md) | Mid-form chunks — still Origin-Story-contaminated; not this pass |

## Persistent artifacts

| File | Purpose |
|------|---------|
| `output/transcript/transcript.txt` | Full transcript (auto on transcribe) |
| `output/plan/manifest.json` | Cut list — agent updates, render reads |

## Workflow

```
input/ → transcribe → output/transcript/ → output/plan/manifest.json → output/deliverables/
```
