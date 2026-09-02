# Hikmat — Content Strategy

Carpentry timelapse project. **Not THP flywheel content** — skip `skills/flywheel_series/` and flywheel stage tagging.

## What this is

A **build timelapse**: one craftsman, multiple sessions, screen/phone recordings of the work. Little or no speech. Visual story = process → finished piece.

## Core hook (use this, not flywheel)

**Result-first, then process** — under 60 seconds.

```
0:00–0:03   FINISHED piece (money shot — best angle, clearest reveal)
0:03–0:55   Process montage (cuts from early → late clips, ascending time)
0:55–1:00   Hold on result OR quick before/after flash
```

Why it works for carpentry shorts:
- Viewer instantly knows *what they're watching for*
- Process satisfies “how it's made” curiosity
- Chronological ascending cuts preserve build logic without needing narration

## Hybrid output mix

| Type | Count (target) | When to use |
|------|----------------|-------------|
| **Montage short** | 8–12 drafts → pick 3–5 | Cross-clip “best of build” compilations |
| **Single-clip short** | 2–3 | Long clips (#5, #11) with one strong 30–45s window |

## Montage rules

1. **Ascending clip order** — never show July before June within one short
2. **Segment length** — 3–5s per cut (TikTok-tight) or 5–8s (Reels-slower)
3. **Total duration** — 30–55s (safe for YT Shorts 60s cap + TikTok + Reels)
4. **Segments per short** — 6–12 cuts, not all 11 clips every time
5. **Short clips** — clips under 15s contribute 1 slice max (see `clip-map.json`)
6. **Avoid** — static UI, loading screens, duplicate angles of the same step

## Segment pool (Layer 1)

Before composing variants, define **candidate windows** per clip on the master timeline.

See [`clip-map.json`](clip-map.json) for exact `master_start` / `master_end` offsets.

Placement heuristic (no speech to guide cuts):
- **Opening** — first visible action (~10% into clip)
- **Middle** — peak activity (~50%)
- **Closing / result** — last clear frame before next clip (~85%)
- **Short clips (<15s)** — one window at ~40% only

Mark winners after a human pass — random timestamps on screen recordings pick dead frames.

## Compose variants (Layer 2)

Generate **10–15 montage recipes**. Each recipe:
- Picks 6–10 segments from different clips
- Enforces ascending order
- Opens with **result slice** (usually from clip #11 or best finish frame)
- Targets 35–55s total

Name pattern: `montage_01`, `montage_02`, …

## Platform targets

Project-specific rules (adapted from platform skills):

| Platform | Skill file | Duration | Notes |
|----------|------------|----------|-------|
| YouTube Shorts | [`skills/youtube_shorts.md`](skills/youtube_shorts.md) | 30–60s | Hard 60s cap |
| TikTok | [`skills/tiktok_shorts.md`](skills/tiktok_shorts.md) | 15–60s | Faster cuts, 3s hook |
| Instagram Reels | [`skills/instagram_reels.md`](skills/instagram_reels.md) | 30–90s | Can breathe slightly longer |

Render **one 9:16 master** per winner first. Platform-specific polish (music, text overlay) is optional pass 2.

## What we skip for hikmat

| Platform default | Hikmat override |
|------------------|-----------------|
| Flywheel stage tagging | Use `hook_type: result-first` |
| Speech-based hooks | Visual result hook |
| Aggressive silence trim | No real audio — skip trim |
| Filler word removal | N/A |
| Transcript-driven cuts | Visual/timeline-driven cuts |
| THP CTA patterns | Simple save/follow or none |

## Manifest conventions (hikmat)

Standard manifest schema uses `flywheel_stage` — for hikmat manifests set:

```json
"flywheel_stage": "n/a",
"hook_type": "result-first",
"content_type": "carpentry-timelapse"
```

Montage shorts use **`segments`** array (multi-cut) instead of single `start`/`end`:

```json
{
  "id": "sh01",
  "title": "Finished table — full build in 45s",
  "hook_type": "result-first",
  "content_type": "carpentry-timelapse",
  "aspect": "9:16",
  "target": "yt-shorts",
  "segments": [
    { "start": 580.0, "end": 585.0, "label": "result-hook" },
    { "start": 5.0, "end": 10.0, "label": "clip01-open" },
    { "start": 200.0, "end": 205.0, "label": "clip05-mid" }
  ],
  "flywheel_stage": "n/a",
  "parent_chapter": "n/a"
}
```

> **Platform gap:** `render_manifest.py` needs `segments[]` support — tracked in capability matrix.

## Workflow

```
clip-map.json          ← timeline offsets (done)
       ↓
segment pool           ← candidate 5s windows per clip (agent + your review)
       ↓
montage recipes        ← 10–15 combos (manifest draft)
       ↓
pick winners           ← you
       ↓
render 9:16            ← render_manifest (after segments support)
       ↓
optional polish        ← music, title overlay
```

## Next step

1. Watch master once — mark **best result frame** (hook source) and 2–3 dead zones to avoid
2. Build segment pool from `clip-map.json`
3. Draft manifest with montage recipes → [`manifest.template.json`](manifest.template.json)
