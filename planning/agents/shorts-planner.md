# Agent: Shorts Planner

**Role:** Extract vertical short clips from chapters, tagged by flywheel stage, sequenced for audience journey.

## Triggers

- Chapters[] drafted in manifest
- Series state available (optional but preferred)

## Inputs

- Full transcript JSON
- `chapters[]` from manifest draft
- `content_pipeline/series/{name}.json` (if series mode)
- Export skill: [`vertical_shorts`](../../skills/vertical_shorts/SKILL.md) — 9:16 file(s) per editorial version
- Script skill: [`situation_resolve`](../../skills/situation_resolve/SKILL.md) — one situation, held until it resolves
- Extraction skill: [`extract_shorts`](../../skills/extract_shorts/SKILL.md) — Hook → Setup → Resolution + coherence gate

## Outputs

- `shorts[]` entries in manifest
- Suggested `publish_queue` ordering

## Skills

- [`skills/plan-stream/SKILL.md`](../../skills/plan-stream/SKILL.md) (shorts phase)
- [`skills/situation_resolve/SKILL.md`](../../skills/situation_resolve/SKILL.md)
- [`skills/extract_shorts/SKILL.md`](../../skills/extract_shorts/SKILL.md)
- [`skills/flywheel-series/SKILL.md`](../../skills/flywheel-series/SKILL.md)
- [`skills/vertical_shorts`](../../skills/vertical_shorts/SKILL.md)

## Instincts

- [content-pipeline.md](../instincts/content-pipeline.md) — "Flywheel" section
- [llm-planning.md](../instincts/llm-planning.md)

## Flywheel Assignment

| Stage | Clip character | CTA direction |
|-------|----------------|---------------|
| attract | Bold hook, open loop | "Full breakdown in [chapter]" |
| engage | Question, polarizing take | "Comment your approach" |
| trust | Personal story, BTS | "More on the channel" |
| service | Quick actionable tip | "Step-by-step in [chapter]" |
| referral | Result, case study | "Client got X — link in bio" |
| loop | Tease next episode | "Part 2 drops [when]" |

Per chapter: target **1–2 shorts** minimum. Assign stages that advance the series, not random hooks.

## Workflow

```
1. Load series state → determine next flywheel stage(s)
2. For each chapter / theme in `shorts_instructions.md`:
   a. Extract transcript slice for the 3–5 min theme block
   b. Name `situation` (problem / issue / struggle / intention) via `situation_resolve`
   c. Apply `extract_shorts`: Hook → Setup → Resolution (or contiguous)
   d. Fail the cut if the situation is not resolved in `coherence.spoken_as`
   d. Write short entry: labeled segments, extract beats, flywheel_stage, parent_chapter, cta
3. Order shorts in publish_queue: flywheel sequence per chapter
4. Update series state with planned clip IDs
```

## Done When

- Each short has valid flywheel_stage enum
- Each short has `extract_mode` + `coherence.complete: true`
- Each short references parent_chapter
- Durations within platform min/max
- No duplicate identical time windows

## Does NOT

- Replace long-form value (shorts tease, chapters deliver)
- Pick chapters (Chapter Planner's job)
- Render video
