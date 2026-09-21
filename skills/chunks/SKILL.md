---
name: chunks
description: Rules for extracting 11 to 15 minute standalone mid-form chapters (16:9).
---

# Mid-Form Chunks (11 - 15 Minutes)

## Content Goal
Extract cohesive, standalone deep-dive chapters from the long stream transcript. The viewer must get full context from start to finish.

## Platform Constraints
- Aspect Ratio: 16:9 (Native Horizontal)
- Min Duration: 660 seconds (11 minutes)
- Max Duration: 900 seconds (15 minutes)
- Silence Removal: Light (Keep natural speech pauses; strip only gaps > 2.5s using auto-editor)

## Timestamp Rules
1. Hook Window (0:00 - 0:45): Must include the setup of a problem, topic introduction, or interesting thesis.
2. Context Guard: Do NOT cut mid-sentence or mid-code explanation. Include 10 seconds of context before the speaker begins the main topic.
3. Natural Outro: End the clip when the speaker transitions to an unrelated topic or completes the conclusion.
4. After the instruction-file chapters are planned, list leftover windows in `deferred_chapters` (or a leftover table). Skipping a 7-min block to hit 15 min is allowed — dropping it without a note is not. Origin Story: `19:50–26:10` (surrender / fake productivity) is short-material, not a chunk; `38:01–45:30` Lebanon/bootcamp and `48:50–52:40` hiring were skipped in ch02; ch03 `52:40–1:07` is the remaining mid-form.

## Tool Execution Output
Pass parameters to `process_stream.py`:
- `--aspect 16:9`
- `--target chunk`
- `--min-len 660`
- `--max-len 900`