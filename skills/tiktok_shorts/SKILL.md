---
name: tiktok-shorts
description: Rules for extracting fast-paced 15 to 60 second vertical TikTok clips.
---

# TikTok Shorts Rules (15 - 60 Seconds)

## Content Goal
Capture immediate, high-retention hooks with high information density, fast pacing, and punchy endings.

## Platform Constraints
- Aspect Ratio: 9:16 (Smart Reframe Centered)
- Min Duration: 15 seconds
- Max Duration: 60 seconds
- Silence Removal: Aggressive (Strip silence gaps > 0.4s using auto-editor)

## Timestamp Rules
1. Instant Hook (0:00 - 0:03): Must start directly on a controversial statement, strong visual reaction, core question, or high-energy point.
2. Pacing: Eliminate fluff, filler words ("um", "ah"), and dead air completely.
3. Sudden Punchline: End immediately after the resolution or punchline is delivered to encourage loop replays.

## Visual & Subtitle Rules
- Subtitles: Burned-in, large centered bold text with yellow/white keyphrase highlight.
- Face Tracking: Apply Smart Crop centering on speaker's face.

## Tool Execution Output
Pass parameters to `process_stream.py`:
- `--aspect 9:16`
- `--target tiktok`
- `--min-len 15`
- `--max-len 60`
- `--auto-editor-tightness aggressive`