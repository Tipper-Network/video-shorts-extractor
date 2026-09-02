# Vision — Long-Form Stream → Themed Library + Flywheel Shorts

> **Scope:** This workspace executes the cut. THP (`the-hard-port-os/`) owns brand strategy, series scripts, and editorial voice. See [`README.md`](README.md#relationship-to-thp).

## Problem

Raw streams (2+ hours) contain multiple standalone topics buried in one file. Manual editing is slow. Single-clip automation ignores theme boundaries and audience journey.

## Goal

Drop one long video → get:

1. **Themed chapters** (10–30 min, 16:9) — each a complete discussion on one subject
2. **Short-form clips** (9:16) — sequenced to move viewers through a relationship flywheel
3. **Series continuity** — posts connect thematically so viewers return for the next beat

## Flywheel Stages

Each short (or post) advances the viewer one step. Loop restarts with new long-form content.

| Stage | Purpose | Viewer state after |
|-------|---------|-------------------|
| **attract** | Curiosity, pain, bold hook | "This is about me" |
| **engage** | Question, debate, participation | "I want to respond" |
| **trust** | Story, transparency, proof of character | "This person is real" |
| **service** | Actionable value, how-to, payoff | "That helped me" |
| **referral** | Case study, result, social proof | "Others got results too" |
| **loop** | Tease next chapter / episode | "I need to see what's next" |

Shorts should **tease** their parent chapter without replacing it. Chapters **deliver** the full value. The loop short bridges to the next stream or episode.

## Success Criteria

- [ ] Full 2hr transcript processed (no arbitrary truncation)
- [ ] Chapters are self-contained (viewer needs no prior context)
- [ ] Chapter boundaries respect natural topic transitions
- [ ] Each chapter yields 1–2 flywheel-tagged shorts
- [ ] Series state tracks theme, episode, and last flywheel stage
- [ ] Human can edit manifest before render
- [ ] Batch render produces organized output tree

## Non-Goals (for now)

- Auto-upload to YouTube/TikTok/Instagram
- Burned-in subtitles and brand overlays
- Face-tracking smart crop (future polish)
- Paid SaaS dependency (local-first: Whisper + FFmpeg; Cursor agent for planning)

## Default Run (no platform specified)

Per master skill fallback:

- All viable themed chapters from the stream
- Minimum 2 vertical shorts, flywheel-tagged
- Output under `content_pipeline/output/{stream_stem}/`
