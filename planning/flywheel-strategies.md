# Flywheel Strategies — Episode vs Shorts

Two peer strategies. Same flywheel **stages** (`attract` → `loop`), different **products** and different **modules**.

Visual overview: [`flywheel-strategies-visual.md`](flywheel-strategies-visual.md)

| | **flywheel-shorts** | **flywheel-episode** |
|--|---------------------|----------------------|
| **Playbook** | [`flywheel-shorts.json`](playbooks/flywheel-shorts.json) | [`flywheel-episode.json`](playbooks/flywheel-episode.json) |
| **Hero product** | Ordered shorts queue | YouTube chapter (+ supporting shorts) |
| **Conclusion for viewer** | Trust built through short sequence | Shorts → full payoff in chapter → loop |
| **Long source role** | Mine — optional library publish | Becomes the chapter (service delivery) |

Pick one per project (or run both on same source for A/B — two manifests).

---

## Strategy A — Flywheel shorts

**The flywheel is the publish queue.** Extract one short per stage (or more for hook acts). Post back-to-back.

```
Source (long video)
       │
       ├─► sh01 attract   ─┐
       ├─► sh02 engage    │
       ├─► sh03 trust     ├─► POST IN ORDER (the journey)
       ├─► sh04 service   │
       ├─► sh05 referral  │
       └─► sh06 loop     ─┘

Optional: publish full source later (library / SEO)
```

### Technical modules

| Module | Role |
|--------|------|
| `transcribe` | Full script |
| `detect_topics` | Concept blocks inside source |
| `plan_manifest` | **shorts-first** — flywheel sequence |
| `render` | Shorts primary; chapters off |
| `polish` | Optional on winners |

### Narrative modules

| Module | Role |
|--------|------|
| `plan_flywheel_sequence` | Map moments → stages; set `publish_order` |
| `plan_chapter` | **Disabled** — service is a short beat, not long-form |

All **4 acts output shorts** (including Serve — a 30–60s value taste).

---

## Strategy B — Flywheel episode

**The chapter is the service delivery.** Shorts wrap it: tease before, proof/loop after.

```
Source (long video)
       │
       ├─► sh01 attract   ─┐  PRE
       ├─► sh02 engage     │  shorts
       ├─► sh03 trust     ─┘
       │
       ├─► ch01 chapter (10–30 min)  ◄── SERVICE (full value)
       │
       ├─► sh04 referral  ─┐  POST
       └─► sh05 loop      ─┘  shorts
```

### Technical modules

| Module | Role |
|--------|------|
| `transcribe` | Full script |
| `detect_topics` | Topic boundaries for chapter cut |
| `plan_manifest` | **Chapter first**, then shorts around it |
| `render` | Chapters (16:9, light trim) + shorts (9:16) |
| `polish` | More common — SFX/zoom on chapter + shorts |

### Narrative modules

| Module | Role |
|--------|------|
| `plan_chapter` | Self-contained 10–30 min; `youtube_chunks` skill |
| `plan_shorts_around_chapter` | Teasers + CTAs; `parent_chapter` required |
| `plan_flywheel_sequence` | **Disabled** — order derived from chapter anchor |

**Deliver act outputs a chapter**, not a short.

---

## Side-by-side: modules

| | flywheel-shorts | flywheel-episode |
|--|-----------------|------------------|
| **Technical: render chapters** | ✗ (optional) | ✓ |
| **Technical: polish** | rare | common |
| **Narrative: plan_chapter** | ✗ | ✓ |
| **Narrative: plan_flywheel_sequence** | ✓ | ✗ |
| **Narrative: plan_shorts_around_chapter** | ✗ | ✓ |
| **Skill: youtube_chunks** | ✗ | ✓ |
| **Short `parent_chapter`** | `n/a` | required |
| **Serve stage lives in** | short (taste) | chapter (full) |

---

## Side-by-side: publish pattern

**flywheel-shorts:**  
`short → short → short → short → short → short`

**flywheel-episode:**  
`short → short → [chapter] → short → short`

---

## Assign to a project

```json
{ "project_id": "thp-campaign-a", "playbook_id": "flywheel-shorts" }
```

```json
{ "project_id": "thp-deep-dive-04", "playbook_id": "flywheel-episode" }
```

Same source video can produce **two manifests** if you want both strategies — different conclusions, different edits.

---

## When to use which

| Choose **flywheel-shorts** when… | Choose **flywheel-episode** when… |
|----------------------------------|-----------------------------------|
| Audience lives on TikTok/Reels/Shorts | Audience expects YouTube deep-dives |
| Trust journey IS the content | Full argument needs 15+ minutes |
| One recording, many scattered beats | One clear topic arc for a chapter |
| Post daily short sequence | Drop chapter with short runway |

---

## Related

- [`playbooks.md`](playbooks.md) — full playbook catalog
- [`vision.md`](vision.md) — flywheel stage definitions
- [`skills/flywheel_series/`](../skills/flywheel_series/SKILL.md) — series continuity
