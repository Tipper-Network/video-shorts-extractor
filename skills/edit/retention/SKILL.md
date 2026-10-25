---
name: edit-retention
description: Edit a signed short or chunk so a stranger stays. First three seconds, an ending that opens the next flywheel stage, and one 9:16 frame. Use after the land is chosen, before render.
---

# Retention

The land is already chosen. This skill is the open, the hold, and the handoff to the next stage. It does not go looking for more shorts. That is [`extract_shorts`](../../extract_shorts/SKILL.md).

## First three seconds

The first line a stranger hears is the situation or its punchline (`hook-first`). By three seconds they know what this film is. That line is speech from the tape. It is not a title card, a sound sting, or a zoom.

`story-first` still opens on the situation, and the punchline is the turn, not a cold open from another story.

## Hold

A short resolves its own situation. An open loop that never lands fails [`situation_resolve`](../../situation_resolve/SKILL.md).

The handoff is the last line plus the Sheet fields `viewer_state` and `next_stage`. The viewer got the land, and the next weekday post is the next state. Do not end on a subscribe line.

A visual change marks a turn in that same situation: a [`dynamic_zoom`](../../dynamic_zoom/SKILL.md) on the admission, a caption emphasis on the land word, or the next splice of the same story. A change every two to four seconds is not the rule. A timer is not a cut.

## Frame

16:9 is fitted to 1080 wide and stacked on a blurred 9:16 ground. The speaker and the board stay in frame. There is no face tracker and no per-platform crop. One file fills Shorts, Reels, and TikTok. Canvas rules: [`vertical_shorts`](../../vertical_shorts/SKILL.md).

Chunks stay 16:9. They are the sit. They do not get the short-form open.

## Graphs

YouTube retention is not pulled. A drop shows up when a person watches the file. The fix is a new out or a new turn, written into the script, then `_v2`.
