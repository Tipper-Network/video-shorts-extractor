# Tipper The Origin Story — Project Index

**ID:** `tipper-the-origin-story`  
**Entity:** **Tipper** (from the title — not `projects/0. the origin story/`)  
**Requirements:** [`requirements.md`](requirements.md)

## Instruction files

| File | When |
|------|------|
| [`shorts_extraction.md`](shorts_extraction.md) | Vertical shorts from this transcript |
| [`chunk_extraction.md`](chunk_extraction.md) | Mid-form chunks (11–15 min), job-first |

## Persistent artifacts

| File | Purpose |
|------|---------|
| `output/transcript/transcript.txt` | Full transcript (auto on transcribe) |
| `output/plan/manifest.json` | Cut list — agent updates, render reads |
| `output/deliverables/shorts/{id}_{slug}.md` | Short playback transcript |
| `output/deliverables/chunks/{id}_{slug}.md` | Chunk playback transcript |

## Workflow

```
input/ → transcribe → output/transcript/ → shorts_extraction.md + chunk_extraction.md
       → playback .md → manifest.json → output/deliverables/
```

Source: `input/2. Tipper _the origin_.mp4` (1:14:16).
