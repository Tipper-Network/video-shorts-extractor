---
name: chunks
description: Plans 11–15 min 16:9 mid-form YouTube chapters. Name one followable job, list 2–3 worked examples, write the structure, then hunt clocks. Use when cutting chunks, chapters, or 10–15 min videos from a speech transcript.
---

# Mid-Form Chunks (11–15 Minutes)

**Planner first. No ffmpeg until the user signs the chunk script.** Resolve entity with [`entity_brand`](../entity_brand/SKILL.md). Craft is [`situation_resolve`](../situation_resolve/SKILL.md) — one situation, held. Shorts punch lives in [`extract_shorts`](../extract_shorts/SKILL.md). This file is the chapter.

A short is one situation that lands. A chunk is **one job someone can follow** — same situation, more examples, more elaboration, a structure they can replay tomorrow.

Do not dump a clock list. The user names which jobs are chapters. Clocks are last.

## Hats (all four, in this order)

| Hat | Decides | Test |
|-----|---------|------|
| **Product** | The job of the 12 minutes | After this, what can they *do*? One sentence they could use. |
| **Marketer** | Is this this entity's queue, and can a person connect? | [`entity_brand`](../entity_brand/SKILL.md) keep / demote / park. Persona (Tipper: Dana / Omar — belong, not sell). |
| **Content** | Is there a script a stranger can follow? | Name / why it sticks / 2–3 examples / copyable order / land. |
| **Editor** | Does the tape hold that script? | Hunt windows. Contiguous if one sitting. Supercut only to skip dead — never to glue two jobs. |

## Chunk vs short

| | Short | Chunk |
|--|-------|-------|
| Unit | One situation | One **job** |
| Body | Punch + enough pressure to land | Same punch **plus** 2–3 examples and the order to use them |
| Duration | 50–75s (floor 50, ceiling 90) | 11–15 min because the examples need room |
| Fail | Two situations glued | Two jobs glued, or a memoir with no method to follow |
| Tipper win | “Show you their world” as a line | “Show you their world” as a method with the triangle, the sell years, the confession |

Elaboration is the product. Pad by holding the same thought (more of the same example family). Do not splice a second job to hit 15:00.

## Workflow (job first)

```
entity_brand          → which queue
product job           → one followable job (list candidates; user marks which are chapters)
content structure     → name / examples / land  → deliverables/chunks/{id}_{slug}.md
situation_resolve     → still one situation; examples are the same situation
editor hunt           → clocks that hold the script
brand pass            → keep / demote / park
user signs the script → then manifest chapters[], then render
leftover scan         → jobs named and not shipped, plus leftover windows
```

1. Resolve `entity`. Read `brands/`.
2. From the transcript, list **jobs** (not clocks). One sentence each, in his spoken words if possible. Write them to `chunk_extraction.md` (or the project’s chunk planner file).
3. **Stop.** The user marks which jobs are chapters. Do not propose `start`/`end` before that.
4. For each kept job, write the script file (template below). `statement` / `pressure` / `resolve` must be quoteable. Examples must be the same situation.
5. Brand pass the chapter the same way as a short. A finished memoir that belongs to founder/GAF/THP is leftover, not a ship on a Tipper title. Tipper: one tip taught thoroughly (People + Places + Events).
6. Hunt the tape. Snap to sentence edges. +10s context before the job starts. Out on a finished land, or when he transitions to an unrelated job.
7. Write `chapters[]` in `manifest.json`. `cut_mode: contiguous` unless dead air requires `supercut`.
8. **Stop.** User approves the script (`script_approved: true`). Then ffmpeg.
9. Leftover table: jobs not shipped, windows skipped to fit 15 min, dead zones. Skipping a 7-min block to hit 15 is allowed — dropping it without a note is not.

## Script file

`output/deliverables/chunks/{id}_{slug}.md`

```markdown
# {id} — {title}

**Entity:** tipper | thp | gaf | founder
**Status:** script — not approved
**Job:** {one sentence they can use tomorrow}
**Situation type:** problem | issue | struggle | intention

| Beat | Must hear (quoteable) |
|------|------------------------|
| **Name** | |
| **Pressure** | |
| **Examples** | 1. …  2. …  3. … |
| **Structure** | the copyable order |
| **Land** | finished clause |

**Playback** (clocks only after the user named this job)

1. …

**spoken_as:** {name}. {pressure}. {example → example}. {land}.

**Skip:** dead air, second jobs, handwriting, "what a stream", time-checks.
**Brand:** keep | demote | park — why
```

`spoken_as` must read as one job. Fail if it changes job without a spoken bridge, if examples are a second story, or if the last sentence is still inside the setup.

## Fail (hard)

- Clocks proposed before the user named the jobs
- Two jobs in one chapter
- Memoir with no followable method (unless entity is founder)
- Under 11:00 or over 15:00 without a flag
- Out mid-clause / mid-explanation
- Hook from a different job
- Instruction-file clocks that belong to another video
- No script `.md`, or ffmpeg before `script_approved`
- Leftover job or skipped window not listed

## Platform

- Aspect: 16:9. Canvas is the source size, capped at 1920 wide — never upscale (720p stays 1280×720).
- Min 660s / max 900s
- Trim: light (keep natural pauses; strip gaps > 2.5s)
- Drafts: `output/deliverables/chunks/`
- Never overwrite a rendered file; next pass is `_v2`, `_v3`, …

## Cut modes

| Mode | When |
|------|------|
| `contiguous` | Default. The job is already one sitting. |
| `supercut` | Same job, skip dead (light checks, board-cap, time-checks). |

Do not supercut two jobs to fit 15 min. Prefer deferring the second job.

## Manifest (after script approval)

```json
{
  "id": "ch01",
  "title": "Find common ground",
  "theme": "common-ground",
  "entity": "tipper",
  "job": "Stop selling look-at-what-I'm-building; find common ground.",
  "cut_mode": "contiguous",
  "aspect": "16:9",
  "target": "chunk",
  "script_file": "output/deliverables/chunks/ch01_common-ground.md",
  "script_approved": false,
  "trim": "light"
}
```

Use `segments[]` only when `cut_mode` is `supercut`. `detect_topics` candidates are Layer 1 — never final.

## Leftover (required)

After the named jobs are scripted, scan the rest. Write `deferred_chapters` or a leftover table: job, neighborhood, verdict (short-material / deferred chunk / dead).

## Tool execution (after approval)

`render_manifest.py --type chapters`

## Does not

- Pick which jobs are chapters (the user does)
- Plan 9:16 (that's `extract_shorts` + `vertical_shorts`)
- Replace `situation_resolve` (craft still gates the throughline)
- Treat Gemini/instruction clocks as the job list when they disagree with the transcript
