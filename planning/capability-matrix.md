# Capability Matrix

Tracks **platform** editing capabilities — scripts and skills — tested against real projects.

**Not project requirements.** For per-job needs see `content_pipeline/projects/{name}/requirements.md`.

## Status key

| Status | Meaning |
|--------|---------|
| `shipped` | Code + skill exist, works reliably |
| `tested` | Ran on a project; known limitations documented |
| `partial` | Works with gaps |
| `planned` | Spec'd, not built |
| `failed` | Tested, needs fix before reuse |

## Core pipeline scripts

| Capability | Script / module | Skill | Status | Tested on | Notes |
|------------|-----------------|-------|--------|-----------|-------|
| Chronological video concat | `concat_clips.py` | — | tested | hikmat | Stream-copy + concat demuxer |
| Normalize portrait / no-audio | `concat_clips.py --mode normalize` | — | tested | hikmat | 6/11 clips re-encoded; cache reused |
| Insert stills in timeline | `concat_clips.py --include-images` | — | failed | hikmat | Split-frame glitches; deferred |
| Whisper transcription | `transcribe.py` / `process_stream.py` | — | shipped | origin-story, tipper-the-story | CPU `small`. Sidecar `.srt` next to `input/` skips Whisper (`--whisper` to force) |
| YouTube SRT → plain + clocks | `srt_to_text.py` | — | tested | program-future-ready | Titled plains in `output/transcript/`; clocked `{n}. {Title}.txt` in each lecture folder |
| GAF lecture → field book | agent | `lecture_ebook` | shipped | program-future-ready | Drop stream wreckage; GAF voice; no Tipper closer |
| Vosk word timestamps | `transcribe.py` | `sfx_allocation` | shipped | — | Needs `VOSK_MODEL_PATH` |
| Agent manifest planning | Cursor agent | `plan_stream` | partial | — | Manual in-session; no script |
| Auto topic detection (heuristic) | `detect_topics.py` | `detect_topics` | shipped | — | Layer 1; agent refines |
| Modular module runner | `run_module.py` | `modules/README` | shipped | — | Per-project enable flags |
| Project pipeline config | `project_config.py` | `project-pipeline.schema` | shipped | hikmat | `projects/{id}/pipeline.json` |
| Visual montage compose | `compose_shorts.py` | hikmat/montage_compose | tested | hikmat | segment pool + manifest |
| Batch render from manifest | `render_manifest.py` | `render_manifest` | tested | hikmat | contiguous + supercut (`-c copy`). Shorts `--jobs 4`. 16:9 no upscale |
| Trim on render | `render_manifest.py` + `trim_profiles.py` | platform skills | shipped | — | light/moderate/aggressive |
| Manual cut render | `process_stream.py --mode render` | — | shipped | — | |
| SFX overlay | `auto-edit.py` + `sfx_resolver.py` | `sfx_allocation` | shipped | — | Synthetic fallback works offline |
| Dynamic zoom | `auto-edit.py` | `dynamic_zoom` | shipped | — | |
| Silence / dead-air trim | `trim_silence.py` + render trim | platform skills | shipped | hikmat skipped | Off for silent projects |
| Filler word removal | auto-editor tight margins | `vertical_shorts` (tiktok variant) | partial | — | Via aggressive trim profile |
| Burned-in subtitles | — | platform skills (spec) | planned | — | Roadmap Phase 6 |
| Smart reframe (face track) | — | — | planned | — | Roadmap Phase 6 |
| Audio noise reduction | — | — | planned | — | |
| Multi-language translation | — | — | planned | — | |

## Platform skills (rules)

| Skill | Path | Status | Tested on | Notes |
|-------|------|--------|-----------|-------|
| Mid-form chunks | `skills/chunks/` | shipped | — | 11–15 min 16:9 rules |
| Vertical shorts | `skills/vertical_shorts/` | shipped | origin-story | 9:16 — editorial versions, not platforms |
| Extract shorts | `skills/extract_shorts/` | shipped | origin-story sh01 | Hook / Setup / Resolution + coherence gate |
| Situation resolve | `skills/situation_resolve/` | shipped | origin-story sh01–sh02 | Script cohesion: situation → pressure → resolve |
| Dynamic zoom | `skills/dynamic_zoom/` | shipped | — | Wired in auto-edit.py |
| SFX allocation | `skills/sfx_allocation/` | shipped | — | Wired via sfx_resolver |
| Plan stream | `skills/plan_stream/` | partial | — | Agent + detect_topics Layer 1 |
| Detect topics | `skills/detect_topics/` | shipped | — | Heuristic blocks + candidates |
| Render manifest | `skills/render_manifest/` | tested | hikmat | supercut + trim wired |
| Flywheel series | `skills/flywheel_series/` | planned | — | |

## Project test log

| Project | Started | Capabilities exercised | Gaps found |
|---------|---------|------------------------|------------|
| **hikmat** | 2026-09-02 | concat, normalize, stills (failed) | 10s pauses, split frames, stills |

## Learnings → platform updates

When a project hits a gap, fix platform then update this table.

| Date | Project | Learning | Platform action |
|------|---------|----------|-----------------|
| 2026-09-02 | hikmat | Stills cause split images at concat | Fix `image_to_video` / concat; retest before next project |
| 2026-09-02 | hikmat | End clips have 10s+ dead air | Build silence-trim skill + auto-editor wrapper |
| 2026-09-02 | hikmat | Portrait + silent clips break naive concat | Shipped normalize path in concat_clips |
| 2026-09-02 | — | Projects need own requirements.md | Added `content_pipeline/projects/` pattern |

## Next platform builds (from hikmat)

Priority order driven by hikmat blockers:

1. **Silence trim** — `trim_silence.py` or auto-editor integration
2. **Stills concat fix** — Ken Burns optional, no split frames
3. **Transcribe hikmat edit base** — validate Whisper path on real project
4. **Burned-in subtitles** — after transcript exists
