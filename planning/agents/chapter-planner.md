# Agent: Chapter Planner

**Role:** Segment a long transcript into themed, standalone 10–30 minute chapters.

## Triggers

- Full transcript available
- Orchestrator or plan script requests chapter plan

## Inputs

- `content_pipeline/subtitles/{stem}.json`
- Platform rules: [`skills/youtube-chunks/SKILL.md`](../../skills/youtube-chunks/SKILL.md)

## Outputs

- `chapters[]` entries for manifest (see [manifest.schema.json](../schemas/manifest.schema.json))

## Skills

- [`skills/plan-stream/SKILL.md`](../../skills/plan-stream/SKILL.md) (chapter phase)
- [`skills/youtube-chunks/SKILL.md`](../../skills/youtube-chunks/SKILL.md)

## Instincts

- [content-pipeline.md](../instincts/content-pipeline.md) — "Chapter boundaries" section
- [llm-planning.md](../instincts/llm-planning.md)

## Workflow (Map-Reduce)

```
1. Split transcript into ~5–10 min blocks by timestamp
2. Cursor agent pass A: label each block (topic, hook_score, is_topic_start)
3. Cursor agent pass B: merge adjacent same-topic blocks → chapter candidates
4. Validate each chapter: 600s ≤ duration ≤ 1800s
5. Snap start/end to sentence boundaries
6. Apply 10s context guard before topic start
7. Assign id (ch01, ch02...), title, theme tag
```

## Planning Principles

- Ask for **all** distinct topics, not "the best one"
- Require self-contained narrative (viewer needs no prior context)
- Never cut mid-sentence
- End at natural topic transition or conclusion

## Done When

- Every chapter within duration bounds OR flagged for human review
- No overlapping chapter time ranges
- Combined chapters cover meaningful portions of stream (gaps OK for dead air/brb)

## Does NOT

- Plan shorts (Shorts Planner's job)
- Render video
- Process only first N segments of transcript
