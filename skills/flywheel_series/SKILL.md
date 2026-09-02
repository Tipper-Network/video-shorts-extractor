---
name: flywheel-series
description: Manages thematic and flywheel-stage continuity across content episodes. Reads and updates series state so shorts advance attract→engage→trust→service→referral→loop. Use when planning shorts for a named series or continuing a content loop.
version: "0.2.0"
status: planned
---

# Flywheel Series State

**Status: planned** — series directory and planner integration pending. See [planning/roadmap.md](../planning/roadmap.md) Phase 4.

## When to Use

- User names a series (e.g. "build-in-public", "client-onboarding")
- Planning shorts that must continue from last episode
- Advancing flywheel stage across publishes

## Vision

Full flywheel definition: [planning/vision.md](../planning/vision.md)

## State Location

```
content_pipeline/series/{series_id}.json
```

Schema: [planning/schemas/series.schema.json](../planning/schemas/series.schema.json)

Example: [planning/templates/series.example.json](../planning/templates/series.example.json)

## Flywheel Stages (order)

```
attract → engage → trust → service → [publish chapter] → referral → loop → (next episode attract...)
```

## Planner Behavior

1. **Read** series file before shorts planning
2. **Set** `next_flywheel_stage` as hint for first short(s) of episode
3. **Assign** stages across shorts in publish_order
4. **Write** planned clip IDs to series (not published until user confirms)
5. **After publish** (manual for now): update `last_flywheel_stage`, increment episode, append to `published[]`

## Shorts Planner Integration

When the Cursor agent plans shorts, include in reasoning:

- `series.theme`
- `episode` number
- `last_flywheel_stage` / `next_flywheel_stage`
- `notes` from series file (human context)

Require output shorts to:
- Match assigned flywheel stage content style
- Include CTA pointing to parent chapter or next episode (loop stage)

## Guardrails

- Never start a new series without explicit `series_id` from user
- Never reset episode counter without user approval
- Prefer advancing one flywheel stage per short, not skipping trust for a hard sell
