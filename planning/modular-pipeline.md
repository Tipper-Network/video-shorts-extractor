# Modular Pipeline — Layering Skills for Flywheel Outcomes

> **Visuals & playbook design:** [`playbooks.md`](playbooks.md) · **Catalog:** [`playbooks/`](playbooks/)

## Goal

Every pipeline action is **separately designed, separately callable**. **Playbooks** combine modules + skills into reusable recipes. Projects assign a playbook and add job-specific overrides.

This lets you compose flywheel stages from reusable blocks instead of one monolithic script.

## Three layers

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 3 — Flywheel sequence (marketing outcome)        │
│  attract shorts → engage → trust → chapter → referral   │
│  Defined in: series.json + agent plan + publish_order   │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│  LAYER 2 — Project workflow (which modules, cut modes)  │
│  projects/{id}/pipeline.json + requirements.md          │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│  LAYER 1 — Callable modules (scripts)                 │
│  transcribe | detect_topics | render | trim | polish    │
└─────────────────────────────────────────────────────────┘
```

## Auto topic detection — what to do

**Do not** rely on a single black-box “AI finds topics” step.

| Step | Module | Output |
|------|--------|--------|
| 1 | `transcribe` | Full timestamped script |
| 2 | `detect_topics` | `{stem}.topics.json` — blocks + chapter **candidates** (heuristic) |
| 3 | `plan_manifest` (agent) | Final `chapters[]` with titles, themes, safe boundaries |
| 4 | Agent shorts pass | `shorts[]` per chapter + flywheel tags |

Heuristic detection uses:
- **Pause gaps** (default ≥2.5s between Whisper segments)
- **Lexical shift** (Jaccard dissimilarity between block word sets)
- **Duration merge** (600–1800s chapter targets from project config)

Future options (not built yet):
- Embedding similarity (local sentence-transformers)
- THP script alignment (match transcript blocks to published outline)

## Supercut vs contiguous — per project

| cut_mode | When | Example project |
|----------|------|-----------------|
| `contiguous` | Speech flows naturally | THP episodes, podcasts |
| `supercut` | Visual montage or scattered highlights | hikmat shorts, “best moments” reels |

Configure in `pipeline.json`:

```json
"chapters": { "cut_mode": "contiguous" },
"shorts":   { "cut_mode": "supercut" }
```

Override any single clip in manifest with `"cut_mode": "supercut"` + `segments[]`.

## Silence / filler trim — wired on render

Trim is a **post-cut module step** inside `render`, not a separate manual pass (unless you call `trim_silence` standalone).

Profiles in `trim_profiles.py` map to platform skills. Per-clip `"trim": "aggressive"` overrides defaults.

Disable for silent projects: `"render": { "trim_on_render": false }`.

## Building a flywheel from modules

Example instruction set you give the agent for a THP episode:

```
1. run_module transcribe --input episode_04.mp4
2. run_module detect_topics --transcript subtitles/episode_04.json
3. Read topics + skills/youtube_chunks → write manifest chapters (contiguous)
4. Read chapters + skills/flywheel_series → write shorts:
   - sh01 attract (from ch01 hook window)
   - sh02 engage (question clip)
   - sh03 trust (proof moment)
   - publish_order 1,2,3 before chapter
5. run_module render --manifest output/episode_04/manifest.json
6. Optional: render --polish for SFX/zoom on winners only
```

Each step is independent — skip detect_topics for hikmat; skip flywheel for timelapse; add compose_shorts instead.

## Files

| File | Role |
|------|------|
| `projects/{id}/pipeline.json` | Module toggles + cut_mode defaults |
| `projects/{id}/requirements.md` | Human intent, audience, constraints |
| `projects/{id}/skills/` | Skill overrides |
| `content_pipeline/modules/README.md` | Module catalog + CLI |
| `planning/schemas/project-pipeline.schema.json` | Config schema |
| `planning/schemas/manifest.schema.json` | Render contract (+ supercut) |

## Agent orchestration

The Cursor agent is the orchestrator — reads `pipeline.json` workflow array, calls modules via `run_module.py` or direct scripts, applies skills between steps, writes manifest, waits for human approval, then renders.

No local Ollama. Heuristic scripts prepare data; agent makes editorial decisions.
