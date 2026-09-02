# Skill Backlog

Skills live in `skills/` at the workspace root. This file tracks what exists, what's planned, and which agent owns each.

## Status Key

| Status | Meaning |
|--------|---------|
| `shipped` | SKILL.md exists and matches current behavior |
| `planned` | Spec'd here; SKILL.md stub may exist |
| `gap` | Referenced but not created yet |

## Platform Skills (shipped)

| Skill | Path | Agent | Notes |
|-------|------|-------|-------|
| youtube-chunks | `skills/youtube_chunks/` | Chapter Planner | 10–30 min 16:9 rules |
| youtube-shorts | `skills/youtube_shorts/` | Shorts Planner | 30–60s 9:16 |
| tiktok-shorts | `skills/tiktok_shorts/` | Shorts Planner | 15–60s aggressive pacing |
| instagram-reels | `skills/instagram_reels/` | Shorts Planner | 30–90s aesthetic |
| dynamic-zoom | `skills/dynamic_zoom/` | Renderer | Periodic zoom in/out |
| sfx-allocation | `skills/sfx_allocation/` | Renderer | Word-triggered SFX |

## Pipeline Skills

| Skill | Path | Status | Agent | Phase |
|-------|------|--------|-------|-------|
| content-pipeline-master | `SKILL.md` | shipped | Orchestrator | 0 |
| plan-stream | `skills/plan_stream/` | planned | Chapter + Shorts Planner | 2 |
| render-manifest | `skills/render_manifest/` | planned | Renderer | 3 |
| flywheel-series | `skills/flywheel_series/` | planned | Shorts Planner | 4 |
| qa-manifest | `skills/qa-manifest/` | gap | QA Reviewer | 5 |

## Skill Creation Order

1. **plan-stream** — unblocks multi-clip planning (highest priority)
2. **render-manifest** — unblocks batch output
3. **flywheel-series** — series continuity
4. **qa-manifest** — automated manifest validation script + checklist

## Mapping: Agent → Skills

```
Orchestrator     → SKILL.md, plan-stream, render-manifest
Transcriber      → (process_stream extract/transcribe only)
Chapter Planner  → plan-stream, youtube-chunks
Shorts Planner   → plan-stream, flywheel-series, youtube-shorts (+ platform)
Renderer         → render-manifest, dynamic_zoom, sfx_allocation
QA Reviewer      → qa-manifest, all platform skills (reference)
```

## When to Create a New Skill

Create a skill when:

- A workflow has repeatable editing steps an agent should follow exactly
- Multiple agents need the same command/schema reference
- Platform-specific cut rules need a dedicated reference doc

Keep one-off judgment in **instincts**, not skills. Keep brand/strategy in **THP**, not here.

## THP vs This Workspace

| Location | Use for |
|----------|---------|
| THP `the-hard-port-os/content/` | Series scripts, observation bank, what to say |
| THP `knowledge/media/youtube/` | Attraction architecture, editorial system |
| `skills/` (this workspace) | How to cut, pace, format, and render |
