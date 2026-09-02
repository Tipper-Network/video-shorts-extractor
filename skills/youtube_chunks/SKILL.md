---
name: youtube-chunks
description: Rules and execution for extracting 10 to 30 minute standalone video chapters.
---

# YouTube Mid-Form Rules (10 - 30 Minutes)

## Content Goal
Extract cohesive, standalone deep-dive chapters from the long stream transcript. The viewer must get full context from start to finish.

## Platform Constraints
- Aspect Ratio: 16:9 (Native Horizontal)
- Min Duration: 600 seconds (10 minutes)
- Max Duration: 1800 seconds (30 minutes)
- Silence Removal: Light (Keep natural speech pauses; strip only gaps > 2.5s using auto-editor)

## Timestamp Rules
1. Hook Window (0:00 - 0:45): Must include the setup of a problem, topic introduction, or interesting thesis.
2. Context Guard: Do NOT cut mid-sentence or mid-code explanation. Include 10 seconds of context before the speaker begins the main topic.
3. Natural Outro: End the clip when the speaker transitions to an unrelated topic or completes the conclusion.

## Tool Execution Output
Pass parameters to `process_stream.py`:
- `--aspect 16:9`
- `--target youtube`
- `--min-len 600`
- `--max-len 1800`