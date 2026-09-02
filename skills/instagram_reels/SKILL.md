---
name: instagram-reels
description: Rules for extracting aesthetic, self-contained 30 to 90 second Instagram Reels.
---

# Instagram Reels Rules (30 - 90 Seconds)

## Content Goal
Focus on practical takeaways, relatable insights, or complete story arcs that appeal to visual and value-driven audiences.

## Platform Constraints
- Aspect Ratio: 9:16 (Smart Reframe Vertical)
- Min Duration: 30 seconds
- Max Duration: 90 seconds
- Silence Removal: Medium (Strip silence gaps > 0.8s)

## Timestamp Rules
1. Visual & Audio Hook (0:00 - 0:05): Ensure clear audio and a readable title overlay introduce the core value immediately.
2. Structure: Prioritize self-contained stories, clear "how-to" advice, or actionable tips.
3. CTA Outro: End with a clean statement that leaves room for a follow/save call-to-action.

## Visual & Subtitle Rules
- Subtitles: Clean modern sans-serif subtitles positioned in the lower-middle third (safe zone for Instagram UI buttons).
- Brand Colors: Apply primary brand color accents to highlighted key terms.

## Tool Execution Output
Pass parameters to `process_stream.py`:
- `--aspect 9:16`
- `--target instagram`
- `--min-len 30`
- `--max-len 90`