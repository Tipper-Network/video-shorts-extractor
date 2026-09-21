---
name: entity-brand
description: Resolve which entity a video belongs to from its title/folder name, then load that entity's brand from brands/ before extracting shorts. Use on every named project (Tipper, THP, GAF).
---

# Entity Brand

The video name is the brand key. **Tipper**, **The Hard Port (THP)**, and **The GAF** are siblings under one philosophy — not one brand wearing three names. Do not collapse them.

**Canonical brand files live in [`brands/`](../../brands/).** Read those first. Do not hunt Desktop copies unless `brands/` is missing a file.

Craft (`situation_resolve`) answers: does the thought finish?  
This skill answers: does this thought belong to **this** entity's queue?

Read this **before** writing `shorts_extraction.md` or `segments[]`.

## Resolve the entity

From folder name, `pipeline.json` `project_id`, source filename, or YouTube title — first matching token wins:

| Token in the name | Entity | Read from `brands/` |
|-------------------|--------|---------------------|
| `tipper` | **Tipper** | [`Tipper_Brand_Book.md`](../../brands/Tipper_Brand_Book.md) |
| `hard port`, `thp`, `the hard port` | **THP** | [`the-hard-port-brief.md`](../../brands/the-hard-port-brief.md) |
| `gaf`, `the gaf`, `the g.a.f.`, `guild` | **GAF** | [`GAF_Brand_Brief.md`](../../brands/GAF_Brand_Brief.md) then [`GAF_Brand_Book_Updated.md`](../../brands/GAF_Brand_Book_Updated.md) |
| `origin story` with no entity token | **founder** | Spoken style only (below). Do not pick shorts as if they were Tipper, THP, or GAF product. |

Write `entity` on the project (`requirements.md` + extraction header). If the name is ambiguous, ask — do not guess THP by default.

## Founder style (always)

How he talks. Applies to every entity. Not a fourth brand.

- Direct, investigative, calm, occasionally sarcastic. No pity, hustle, empty reassurance. (`USER.md` + Origin Story cuts: situation → pressure → resolve; 50–75s; last clause finished.)
- THP observational filming-map delivery (seated / slow / controlled frustration) is **THP-only**. Do not put it on a Tipper or GAF title.

## Entity filters (from `brands/`)

Same belief underneath: assumptions, not lack of effort, slow people down. Different medium:

| Entity | From the book | Keep shorts that… | Kill / park |
|--------|---------------|-------------------|-------------|
| **Tipper** | People + Places + Events. Tagline **one tip at a time**. Everyman: belong, connect, equal footing. Voice: friendly, practical, authentic, candor, no jargon. Entities (shops, NPOs, creatives) and users. | Common ground with a community; seeing their world; people/places/events (somewhere / something / someone); dump knowns so you can hear; don't sell the product. | Feature lists. THP “you're oblivious / apply now.” GAF guild-hall as the closer. Career-switcher memoir unless it teaches how you meet a community. |
| **THP** | No-bullshit media for SMBs that are “doing fine.” Fine is the problem. **We give a f\*ck. We just don't care.** Nautical: sea, sail, port, rocks, drift. Second person. Banned: unlock, leverage, empower, seamless, game-changer, boost. Never name Tipper on a THP public cut. | Survival-mode; attention vs demand; branding vs evidence; you're not going anywhere. | Tipper-as-the-product. GAF adventure. Reassurance. Announcing honesty. |
| **GAF** | Guild of Adventurers and Frontiers. Not a school. **Assumptions kill growth.** Shackleton-honest. Play as method, not hustle. Presence / room / body. Other guilds run on Tipper — don't make Tipper the closer of a GAF short. | Frontier, being guided not taught, assumptions, play-as-method. | Hustle. Startupy pitch-deck. THP funnel copy. Tipper donations/software as the ending. |
| **founder** | Autobiography that feeds all three. | A thought that finishes. Tag leftover Tipper / THP / GAF later if a line clearly belongs. | Treating Origin Story as a Tipper launch or a THP FND video. |

Internal chain (from the THP brief — **not for public THP copy**): Hard Port (testing) → research framing → Tipper (platform). Silence about the door beyond Hard Port is the gate.

## Workflow

1. Resolve `entity` from the name. Write it on `requirements.md`.
2. Read that row’s file(s) in `brands/`.
3. Run craft (`situation_resolve` + `extract_shorts`) on the transcript.
4. **Brand pass:** keep / demote / park against the entity table. Publish_order is the entity flywheel, not “every complete thought.”
5. Caption/overlay distinctions from that book only:
   - Tipper: people / places / events, one tip, belong vs sell
   - THP: attention / demand / evidence, drift / port, you vs you
   - GAF: assumption / frontier / guide
   Do not mix vocabularies on one short.

## Does not

- Replace situation_resolve (craft still gates the splice)
- Let THP observational series rules ride onto a Tipper-titled video
- Use Desktop copies when `brands/` has the file
