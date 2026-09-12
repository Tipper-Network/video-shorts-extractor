# {Project Name} — Project Index

**ID:** `{project-id}` — set in `pipeline.json`  
**Requirements:** [`requirements.md`](requirements.md)

## Instruction files

Add persistent briefs here (do not regenerate in chat):

| File | When to add |
|------|-------------|
| `shorts_instructions.md` | Vertical shorts / flywheel clips |
| `youtube_instructions.md` | Mid-form or long-form YouTube chapters |
| `{platform}_instructions.md` | Any other platform-specific brief |

## Persistent artifacts

| File | Purpose |
|------|---------|
| `output/transcript/transcript.txt` | Full transcript (auto on transcribe) |
| `output/plan/manifest.json` | Cut list — agent updates, render reads |

## Workflow

```
input/ → transcribe → output/transcript/ → output/plan/manifest.json → output/deliverables/
```
