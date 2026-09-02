# Hikmat — Project Requirements

Project-specific edit requirements. Platform code/skills are shared; this file is **only for hikmat**.

- **Platform capabilities:** [`planning/capability-matrix.md`](../../planning/capability-matrix.md)
- **Project index:** [`brief.md`](brief.md)

---

## Identity

| Field | Value |
|-------|-------|
| Project ID | `hikmat` |
| Series JSON | `content_pipeline/series/hikmat.json` |
| Source folder | `~/Desktop/hikmat-project/` |
| Output folder | `content_pipeline/output/hikmat/` |

## Goal

> **Phase 1:** Concat all raw clips into **one big timeline** (~10 min). ✓  
> **Phase 2:** Cut **vertical timelapse shorts** — result-first hook, process montage, ≤60s.

Stills deferred. Master is clean. See [`content-strategy.md`](content-strategy.md) for shorts planning.

## Audience & outputs

- **Audience:** Carpentry / maker / timelapse viewers
- **Phase 1 output:** One connected 16:9 master — `hikmat_timeline_normalized.mp4` ✓
- **Phase 2 output:** Multiple 9:16 shorts — montage + single-clip variants
- **Hook:** Finished piece first → process montage (ascending clip order)
- **Target length:** Shorts 30–60s (platform-specific — see `skills/`)

## Source assets

| Rule | Value |
|------|-------|
| Sort order | Filename timestamp `YYYYMMDD_HHMMSS` |
| Exclude | `one.mp4` (duplicate), incomplete `.crdownload` |
| Include stills? | **Deferred** — caused split-frame glitches |
| Stills available | `20260730_115835.jpg`, `20260731_121250.jpg` |

### Clip order (11 videos)

| # | File | Duration | Audio track | Notes |
|---|------|----------|-------------|-------|
| 1 | `20260609_104427.mp4` | 79.8s | yes | |
| 2 | `20260609_120526.mp4` | 8.3s | **none** | screen/silent |
| 3 | `20260609_130550.mp4` | 37.3s | **none** | screen/silent |
| 4 | `20260609_131730.mp4` | 67.3s | yes | portrait |
| 5 | `20260609_135326.mp4` | 158.9s | **none** | longest clip |
| 6 | `20260610_170726.mp4` | 39.7s | yes | likely silent content |
| 7 | `20260610_172456.mp4` | 54.3s | yes | likely silent content |
| 8 | `20260629_150318_1.mp4` | 16.1s | **none** | screen/silent |
| 9 | `20260704_161753_1.mp4` | 8.9s | yes | likely silent content |
| 10 | `20260730_115350.mp4` | 30.9s | yes | portrait |
| 11 | `20260730_115546.mp4` | 108.6s | yes | likely silent content |

**4 clips have no audio track at all.** Others may have a track but be naturally silent (screen recordings) — that is **fine**, not a defect.

### Two different problems — don't conflate

| Type | What it is | Action |
|------|------------|--------|
| **Silent by nature** | Screen recordings, no mic — clip is meant to have no sound | Leave as-is; optional music/SFX in polish pass |
| **Static screen / freeze (edit bug)** | Same frame held too long, split image, concat glitch — **our pipeline broke it** | Fix in editing: cut section, re-encode, or exclude bad segment |

The long "pauses" and split frames on end clips are **edit issues**, not content. Silent clips are **not**.

### Audio / silence trim — **skip for hikmat**

- **Do not use audio-based silence trim** — useless when there's no real audio, harmful on synthetic silent tracks.
- **Do not treat silent clips as broken** — they're expected for this project.
- **Do fix:** static/frozen sections caused by bad concat or corrupt segments (manual cut or re-encode).

## Edit requirements

### Assembly
- [x] Chronological concat
- [x] Normalize portrait + missing-audio clips
- [ ] Insert stills (blocked — needs platform fix for split images)

### Pacing & fixes
- [ ] Cut **static/freeze sections** — editing artifacts (concat glitches, held frames)
- [ ] **Silent clips** — no action needed; not a pacing problem
- [ ] Manual review after full re-encode master is ready

### Visual
- [ ] Fix split-frame glitches (end clips + still attempt)
- [ ] Subtitles: _TBD_
- [ ] Dynamic zoom: _TBD_

### Audio
- [ ] SFX: _TBD_
- [ ] Music: _TBD_

## Clips to cut

_None confirmed yet._ Review after watching edit base.

## Known issues

| Issue | Location | Status |
|-------|----------|--------|
| Pauses / static screens | End clips, bad concat | open — **edit bug**, cut or re-encode |
| Naturally silent clips | 4+ screen recordings | expected — **not a bug** |
| Stills concat | JPG → video segments | deferred |

## Decisions log

| Date | Decision | Notes |
|------|----------|-------|
| 2026-09-02 | Videos-only normalized concat | Stills removed until platform handles them |
| 2026-09-02 | Silent clips ≠ broken clips | Screen recordings stay silent; only fix static/freeze edit artifacts |

## Current artifacts

| Artifact | Path |
|----------|------|
| Edit base | `content_pipeline/output/hikmat/hikmat_timeline_normalized.mp4` |
| Normalized cache | `content_pipeline/output/hikmat/normalized/` |

## Workflow

```
11 raw clips  →  ONE master (16:9)  →  segment pool  →  montage manifest  →  SHORT snippets (9:16)
     ✓ done           ✓ done              next               next                  pending
```

Planning docs: [`content-strategy.md`](content-strategy.md) · [`clip-map.json`](clip-map.json) · [`skills/`](skills/)

## Status

| Step | Phase | Status | Artifact |
|------|-------|--------|----------|
| Concat → one big video | 1 | **done** | `hikmat_timeline_normalized.mp4` (~610s) |
| Master review (hook + dead zones) | 2 | optional | adjust manifest timestamps |
| Segment pool | 2 | **done** | `output/hikmat/segment-pool.json` (28 candidates) |
| Montage manifest | 2 | **done** | `output/hikmat/manifest.json` (11 shorts) |
| Render shorts (9:16) | 2 | **done** | `output/hikmat/shorts/` (11 drafts) |
| Pick winners + tweak timestamps | 2 | **next** | review manifest |
| Stills insert | — | deferred | |
| Polish (music/text overlay) | 2 | pending | optional pass 2 |
