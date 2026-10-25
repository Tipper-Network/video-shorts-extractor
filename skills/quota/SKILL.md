---
name: quota
description: Future posting strategy. Fill the weekday quota from flywheel-tagged videos. Not the way a cut is chosen.
status: future
---

# Quota

**Status: future.** Selection and brand decide the cut. This file is how a later posting strategy drains signed videos. The live pipe is [`publish_schedule`](../publish_schedule/SKILL.md). The two strategy shapes are in [`planning/flywheel-strategies.md`](../../planning/flywheel-strategies.md).

Demand is the calendar. The bin is signed videos. The flywheel is the order the bin drains. Cutting stays in [`extract_shorts`](../extract_shorts/SKILL.md) and [`chunks`](../chunks/SKILL.md).

## Demand

- Five posts a week. Monday through Friday. One video a day. Weekends empty.
- One file. YouTube, Shorts, Reels, and TikTok are uploads of that file, not new cuts.
- Asia/Beirut. Date only. Dokploy posts the oldest `scheduled` row.

## The row

Each video carries one `flywheel_stage`:

`attract → engage → trust → service → referral → loop`

Also `publish_order`, `viewer_state`, and `next_stage`. Those four fields are how the next post knows what the viewer was just left with.

`content_pillar` is the old weekday map. The slot is filled by `flywheel_stage`.

## Fill

1. Bin = signed videos that are not already `scheduled` or `posted`.
2. Next empty weekday after the last scheduled date. Do not move the live queue.
3. Place the next bin video in flywheel order. A stage with several videos waits its turn and posts again when the wheel comes back around.
4. A stage with nothing in the bin is skipped. The weekday still gets a video. Do not invent a cut to fill a missing stage.
5. On flywheel-episode, service is the chunk. It takes a weekday when it is signed. It is not also a short of the same job.

## What this skill does not do

- Choose the in and out. That is supply, then the edit subcategories.
- Set `status=scheduled`. A human does that.
- Reschedule the ten chunks already public on The G.A.F.
