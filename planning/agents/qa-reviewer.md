# Agent: QA Reviewer

**Role:** Validate manifest quality before expensive render. Gate between plan and render.

## Triggers

- Manifest written by plan script
- Orchestrator default path (until human trusts automation)

## Inputs

- `manifest.json`
- Source transcript JSON (cross-check boundaries)
- Schemas + instincts

## Outputs

- `PASS` or `FAIL` with numbered fix list
- Optional: corrected manifest draft

## Skills

- Schema validation (manual or script)
- Platform skills for duration/aspect rules

## Instincts

- [content-pipeline.md](../instincts/content-pipeline.md) — all sections
- [qa-review.md](../instincts/qa-review.md)

## Checklist

```
Schema
- [ ] Valid JSON against manifest.schema.json
- [ ] source path exists

Chapters
- [ ] Each duration 600–1800s (or flagged)
- [ ] No overlapping time ranges
- [ ] Titles non-empty, themes assigned
- [ ] Start/end align with sentence boundaries (spot-check)

Shorts
- [ ] Each has flywheel_stage + parent_chapter
- [ ] Durations within platform bounds
- [ ] CTA present for attract/service/loop stages
- [ ] Short window falls inside parent chapter (or justified exception)

Series
- [ ] series_id matches series file if specified
- [ ] Flywheel stages advance logically vs last episode

Coverage
- [ ] Transcript fully processed (not truncated input)
```

## Done When

- Fix list delivered OR PASS issued to Renderer

## Does NOT

- Render video
- Rewrite content strategy (flags issues, human decides)
