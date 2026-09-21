# The Origin Story — Requirements

**Project ID:** `origin-story`  
**Entity:** `founder` (title has no Tipper / THP / GAF token — autobiography, not a product queue)  
**Playbook:** `flywheel-shorts` (+ mid-form chunks)

## Instruction files (source of truth)

Do not recreate these in chat — read and update manifest from them:

| File | Creative brief |
|------|----------------|
| [`shorts_instructions.md`](shorts_instructions.md) | 5 vertical short concepts |
| [`chunk_instructions.md`](chunk_instructions.md) | 3 mid-form chapter concepts (batch 1 renders 2) |

## Deliverables (batch 1)

| Output | Count | Skill | Path |
|--------|-------|-------|------|
| **Shorts (9:16)** | 5 concepts (up to 3 editorial versions) | [`skills/extract_shorts`](../../skills/extract_shorts/SKILL.md) + [`skills/vertical_shorts`](../../skills/vertical_shorts/SKILL.md) | scripts + drafts: `output/deliverables/shorts/` · signed-off: `output/deliverables/shorts_approved/` |
| **Mid-form chunks (16:9)** | 2 | [`skills/chunks`](../../skills/chunks/SKILL.md) | `output/deliverables/chunks/` |

One file per editorial version. Not YouTube / TikTok / Reels copies.

**Batch 2:** `ch03` deferred — see `chunk_instructions.md` Video 3.

## Goal

Repurpose the 1:07:30 livestream into:
- **Shorts queue** — flywheel clips on YouTube, TikTok, and Reels
- **Mid-form chapters** — two documentary-style YouTube uploads (11–15 min)

**Related video (all outputs):** [The Origin Story](https://studio.youtube.com/video/PJfvjQMPbGo)

## Source

| Field | Value |
|-------|-------|
| Input | `input/0. Origin story.mp4` |
| Runtime | ~67 min |

## Outputs

| Artifact | Path |
|----------|------|
| Transcript (always) | `output/transcript/transcript.txt` |
| Segment JSON | `output/transcript/segments.json` |
| Edit plan | `output/plan/manifest.json` |
| Renders | `output/deliverables/{shorts,chunks}/` |

## Edit rules

### Shorts (from shorts_instructions.md + vertical_shorts skill)
- 9:16, blurred background reframe (shrink 16:9 to width); whiteboard punch-in = polish pass
- Platform trim on render (moderate / aggressive / medium)
- Captions / kinetic text / banners = phase 2

### Chunks (from chunk_instructions.md + chunks skill)
- 16:9, 11–15 min target after trim
- Trim stream dead space (>0.4s), normalize -14 LUFS
- Punch-in 1.2–1.3x on emotional beats; board pan when diagrams referenced
- Tangent trims noted per chapter in manifest `edit_notes`

## Queues

**Shorts:** sh01–sh05 — see `shorts_instructions.md`  
**Chunks (batch 1):** ch01–ch02 — see `chunk_instructions.md` Videos 1–2

Draft cuts in `output/plan/manifest.json` — refine against `transcript.txt`.
