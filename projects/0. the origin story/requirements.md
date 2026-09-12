# The Origin Story — Requirements

**Project ID:** `origin-story`  
**Playbook:** `flywheel-shorts` (+ mid-form YouTube chapters)

## Instruction files (source of truth)

Do not recreate these in chat — read and update manifest from them:

| File | Deliverables |
|------|--------------|
| [`shorts_instructions.md`](shorts_instructions.md) | 5 × 9:16 shorts (30–60s) |
| [`youtube_instructions.md`](youtube_instructions.md) | 3 × 16:9 chapters (11–15 min) |

## Goal

Repurpose the 1:07:30 livestream into:
- **Shorts queue** — flywheel clips driving to full video
- **Mid-form chapters** — three documentary-style YouTube uploads

**Related video (all outputs):** [The Origin Story](https://studio.youtube.com/video/PJfvjQMPbGo)

## Source

| Field | Value |
|-------|-------|
| Input | `input/0. Origin story.mp4` |
| Runtime | ~67 min |

## Outputs

| Deliverable | Path |
|-------------|------|
| Transcript (always) | `output/transcript/transcript.txt` |
| Segment JSON | `output/transcript/segments.json` |
| Edit plan | `output/plan/manifest.json` |
| Renders | `output/deliverables/youtube/` |

## Edit rules

### Shorts (from shorts_instructions.md)
- 9:16, center crop; whiteboard punch-in = polish pass
- Trim silence on render
- Captions / kinetic text / banners = phase 2

### Chapters (from youtube_instructions.md)
- 16:9, trim stream dead space (>0.4s), normalize -14 LUFS
- Punch-in 1.2–1.3x on emotional beats; board pan when diagrams referenced
- Tangent trims noted per chapter in manifest `edit_notes`

## Queues

**Shorts:** sh01–sh05 — see `shorts_instructions.md`  
**Chapters:** ch01–ch03 — see `youtube_instructions.md`

Draft cuts in `output/plan/manifest.json` — refine against `transcript.txt` after transcribe.
