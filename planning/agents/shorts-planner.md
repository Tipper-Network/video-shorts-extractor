# Agent: Shorts Planner

**Role:** Extract vertical short clips from chapters, tagged by flywheel stage, sequenced for audience journey.

## Triggers

- Chapters[] drafted in manifest
- Series state available (optional but preferred)

## Inputs

- Full transcript JSON
- `chapters[]` from manifest draft
- `content_pipeline/series/{name}.json` (if series mode)
- Platform skill: default [`youtube-shorts`](../../skills/youtube-shorts/SKILL.md); also tiktok, instagram as requested

## Outputs

- `shorts[]` entries in manifest
- Suggested `publish_queue` ordering

## Skills

- [`skills/plan-stream/SKILL.md`](../../skills/plan-stream/SKILL.md) (shorts phase)
- [`skills/flywheel-series/SKILL.md`](../../skills/flywheel-series/SKILL.md)
- Platform short skills (youtube-shorts, tiktok-shorts, instagram-reels)

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
2. For each chapter:
   a. Extract transcript slice for chapter window
   b. Cursor agent: find 1–2 moments matching stage + platform duration
   c. Write short entry: start, end, title, flywheel_stage, parent_chapter, cta
3. Order shorts in publish_queue: flywheel sequence per chapter
4. Update series state with planned clip IDs
```

## Done When

- Each short has valid flywheel_stage enum
- Each short references parent_chapter
- Durations within platform min/max
- No duplicate identical time windows

## Does NOT

- Replace long-form value (shorts tease, chapters deliver)
- Pick chapters (Chapter Planner's job)
- Render video
