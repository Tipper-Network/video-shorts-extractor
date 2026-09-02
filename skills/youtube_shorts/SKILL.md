---
name: youtube-shorts
description: Rules for 30 to 60 second YouTube Shorts designed to drive traffic back to the channel.
---

# YouTube Shorts Rules (30 - 60 Seconds)

## Content Goal
Provide high-value snippets that spark curiosity and act as teasers for long-form channel content.

## Platform Constraints
- Aspect Ratio: 9:16 (Vertical)
- Min Duration: 30 seconds
- Max Duration: 60 seconds (Hard cap)
- Silence Removal: Moderate (Strip gaps > 0.6s)

## Timestamp Rules
1. High-Curiosity Hook: Focus on fascinating technical concepts, deep "did you know" facts, or surprising outcomes.
2. Narrative Arc: Provide a quick mini-payoff while leaving the broader context open for the main video.

## Tool Execution Output
Pass parameters to `process_stream.py`:
- `--aspect 9:16`
- `--target yt-shorts`
- `--min-len 30`
- `--max-len 60`