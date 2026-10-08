---
name: story-snippet
description: >-
  Extract a self-contained short-story vignette (300–800 words) from long
  transcript or text, preserving original phrasing, narrative arc, and a
  3–6 word title as JSON — plus flywheel_stage, viral hashtags, and a
  flywheel-aware description for later post packs. Use when hunting
  story-shaped shorts candidates, vignette extraction, storyline discovery
  before situation_resolve / extract_shorts, or scoring external clip packs
  (e.g. Opus) as moment scouts.
disable-model-invocation: true
---

# Story Snippet

**Discovery only. No ffmpeg. No `segments[]`.** Finds story-shaped prose windows that feed [`extract_shorts`](../extract_shorts/SKILL.md). Script cohesion stays in [`situation_resolve`](../situation_resolve/SKILL.md). Entity filter stays in [`entity_brand`](../entity_brand/SKILL.md). Viral polish (captions / sounds) is step-2 — never part of this skill.

## When

- After `output/transcript/transcript.txt` exists (or the user pastes long source text)
- Before writing `segments[]` or encoding drafts
- When hunting leftover storyline candidates the instruction file missed
- When the user asks for vignette / short-story / storyline extraction from a long talk
- When an external clip pack lands (e.g. `opusclip-shorts/`) and you need to learn **moments**, not ship their edits

## System instructions

You are an expert story editor. Your task is to extract a self-contained "short story" scene or vignette directly from a long text, preserving narrative flow and emotional resonance.

RULES:
1. DO NOT SUMMARIZE. Do not write "This scene is about...". Extract the actual narrative prose.
2. Ensure the snippet has a clear narrative arc: a beginning hook, a core moment or conflict, and a satisfying ending or Beat.
3. Keep the extracted text between [300 - 800] words. You may trim minor fluff or bridge two consecutive paragraphs for cohesion, but keep original phrasing intact.
4. Generate a compelling, contextually relevant Title (3–6 words) for the extracted snippet — earned from the prose, not clickbait.
5. Assign one `flywheel_stage` and write pack metadata for virality **without lying about the story** (see Pack metadata below).

OUTPUT FORMAT (JSON):
```json
{
  "title": "Generated Short Story Title",
  "story_snippet": "The extracted prose content...",
  "word_count": 412,
  "flywheel_stage": "trust",
  "description": "Flywheel-aware post description (see rules).",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}
```

## Pipeline bridge

300–800 words ≈ the **3–5 min theme block** in [`extract_shorts`](../extract_shorts/SKILL.md). It is the search window, not the shipped short (still **50–75s** after craft; floor 50s).

```
transcript / long text
        ↓
  story_snippet          ← this skill (prose + title + optional clocks)
        ↓
  shorts_extraction.md   ← add candidate theme rows from titles
        ↓
  situation_resolve      ← name situation / pressure / resolve
        ↓
  extract_shorts         ← timestamps → segments[] → script .md
        ↓
  (later) viral stage1–2 ← captions + sounds — not here
```

External clip packs (Opus, etc.) enter as **scouts only**:

```
opusclip-shorts/*.mp4  (or similar)
        ↓
  score each moment  ← this skill's "External scout" section
        ↓
  keep → story_snippets.json + theme row
  kill → note why (entity mash / soft open / clickbait / no resolve)
        ↓
  never promote their burn-in, titles, or crop as the cut
```

### Workflow

0. Resolve `entity` with [`entity_brand`](../entity_brand/SKILL.md) when this is a named project job.
1. Read `output/transcript/transcript.txt` (or the pasted source). Prefer timed transcript lines when present.
2. Extract one or more vignettes. Each must obey the system rules above.
3. When the source is timed, attach clocks on each object (pipeline fields — do not invent story prose):

```json
{
  "title": "Reaction Versus Response",
  "story_snippet": "…original phrasing…",
  "word_count": 412,
  "source_start": 350,
  "source_end": 588,
  "source_clock": "05:50–09:48",
  "entity": "founder",
  "verdict": "keep",
  "flywheel_stage": "trust",
  "description": "I asked if there was a 5% chance I was an idiot. First thing I did was say no. That was a reaction. Managing the business, friends, communication, studying — that was giving myself a chance to respond.\n\nViewer state after: this person is real.\nNext in flywheel: service — the move you make once you stop defending.",
  "hashtags": [
    "#ReactionVsResponse",
    "#OriginStory",
    "#SelfHonesty",
    "#FounderLife",
    "#BuildInPublic"
  ]
}
```

`source_start` / `source_end` are seconds. Omit clocks only when the source has none. `description` + `hashtags` + `flywheel_stage` are always required on keep/ab (optional on park/kill, but stage still helps).
4. Write the array to `output/plan/story_snippets.json`. Also print each object in chat.
5. Promote survivors into `shorts_extraction.md` / `shorts_instructions.md` as theme rows (`title`, idea, candidate neighborhood from clocks, `flywheel_stage`).
6. Hand off: run [`situation_resolve`](../situation_resolve/SKILL.md), then [`extract_shorts`](../extract_shorts/SKILL.md). Fail the craft gate → discard or widen the window; do not force a splice from a pretty title. Carry `flywheel_stage` / `description` / `hashtags` forward into the short's script `.md` and later post pack when present.
7. **Stop.** Do not render until the user approves the script from extract_shorts.

### Pack metadata (virality format + flywheel)

Stay as close as possible to viral short **form** (mute-first hook in the description, searchable tags) while the **story** stays his words. Link every pack field to the flywheel in [`planning/vision.md`](../../planning/vision.md).

| `flywheel_stage` | Viewer state after | Description must… |
|------------------|--------------------|-------------------|
| `attract` | "This is about me" | Open on pain / curiosity; no soft setup |
| `engage` | "I want to respond" | End on a question or tension the viewer can answer |
| `trust` | "This person is real" | Land on a lived beat (night, denial, decision) |
| `service` | "That helped me" | Name the usable move without a lecture title |
| `referral` | "Others got results too" | Show outcome / proof, not a pitch deck |
| `loop` | "I need what's next" | Point at the next stage or chapter without spoiling it |

**`description` rules**

- 2–5 short paragraphs (or line breaks) ready to paste into YouTube / Insta / TikTok later.
- Line 1 = mute-scroll hook (situation or punch), earned from the vignette.
- Middle = pressure in plain speech (paraphrase OK here; do **not** rewrite `story_snippet`).
- Close = resolve beat + one flywheel line: `Viewer state after: …` and `Next in flywheel: {stage} — …`.
- No "Unlock your potential" / hustle / fake urgency. Founder voice: direct, calm, occasionally sharp.
- Entity name only when the vignette is truly that brand (Tipper / GAF / THP); founder Origin Story stays autobiographical.

**`hashtags` rules**

- 4–8 tags, each starting with `#`, CamelCase or plain; no spaces inside a tag.
- Mix: **1–2 theme tags** from this vignette + **1–2 entity/series tags** + **1–3 discovery tags** that a stranger might search (the virality layer).
- Prefer specific (`#ReactionVsResponse`, `#SleepingOutsideTheCafe`) over empty growth stacks (`#Motivation`, `#SuccessMindset`, `#LevelUp`) unless the prose truly is that.
- Never paste Opus's generic cloud unchanged. Never tag a sibling entity the vignette does not belong to.
- When an entity has a fixed bank later (`brands/assets/{entity}/`), prefer that bank + 2–3 theme tags from this story.

### Selection instincts

- Prefer **lived scenes** (a bet, a denial, a night, a storm, a decision) over abstract lists or framework lectures.
- One vignette = one arc. Do not glue two unrelated stories to hit the word floor.
- Trim filler ("um", "sorry", "let's do this", handwriting asides) — that is fluff, not paraphrase.
- Bridging consecutive paragraphs is allowed only to keep flow; do not rewrite voice.
- Title must be usable as a short slug later (3–6 words). **No clickbait the prose does not earn** (reject Opus-style: "Unlock Your Strengths", "My Simple Strategy" unless those words are the land).
- Soft / meandering opens ("I need to ask like in the water quality menu…") are not hooks — start at the first line that names the situation, or fail the window.
- Entity mash (Tipper + GAF + THP in one vignette) → **park** or split. Sibling brands stay separate per [`entity_brand`](../entity_brand/SKILL.md).
- A beautiful 15–30s bite is a **scout hint**, not a ship. Widen to 300–800 words so extract_shorts can still clear the 50s floor with a full resolve.

### Fail / reject

- Paraphrase or summary disguised as extraction
- Word count outside 300–800
- No ending beat (setup only / open loop)
- Needs a whiteboard, prior chapter, or name the viewer never gets inside the snippet
- Two situations smashed together with no spoken bridge
- Title sells a different story than the prose
- Soft open left in as the first sentence of the vignette
- Cross-entity product pitch mashed into a founder autobiography (or the reverse)
- Missing `flywheel_stage`, `description`, or `hashtags` on a keep/ab object
- Description that is clickbait / hustle and does not match the vignette's resolve
- Hashtag cloud of empty growth tags with no theme tags from the prose

## External scout (Opus / clip packs)

Use when the user drops finished clips under something like `step-2-viral-edit/opusclip-shorts/` (or shares Opus exports). Goal: harvest **moments**, not their captions, crop, watermark, or marketing titles.

For each complete `.mp4` (skip `.crdownload`):

1. Note duration and Opus title (for reference only).
2. Transcribe or read enough speech to name the situation in one sentence.
3. Map to the long transcript clocks when possible (`source_start` / `source_end`).
4. Score:

| Verdict | When |
|---------|------|
| **keep** | One lived arc; fits this job's entity; can widen to 300–800 words with a resolve |
| **ab** | Same theme as an existing short (e.g. reaction/response) — A/B the window, do not replace a signed cut blindly |
| **park** | Real story but wrong entity, or needs a dedicated job |
| **kill** | Soft open, no resolve, entity mash, clickbait-only, incomplete download |

5. Append keep/ab/park entries to `story_snippets.json` with `"scout": "opus"` (or the pack name) and `"opus_title"` for traceability. Still require `flywheel_stage`, `description`, and `hashtags` on keep/ab — rewrite pack copy in our voice; do not paste Opus titles/hashtags.
6. Never copy their kinetic captions, green highlight, emoji, or logo into our cut plan.

### Origin Story pack (worked scout — 2026-09-23)

Long source: founder Origin Story. Pack folder: `opusclip-shorts/`.

| Opus title (ignore as ship title) | ~Dur | Moment | Verdict | Ours |
|-----------------------------------|------|--------|---------|------|
| Cafe Owner → Sleeping Outside | 29s | Closed cafe, broke, sleeping outside the restaurant | **keep** | New leftover vignette — widen in transcript |
| GAF & THP Birthplace | 22s | Names GAF, THP, Tipper in one breath | **park** | Entity mash; not founder-only |
| Stop Reacting, Start Responding… | 95s | Reaction → respond | **ab** | Same arc as signed `sh01`; compare windows, keep our story-first unless user prefers theirs |
| Storm Rescue | 17s | Helped with boat in a storm, got fish | **keep** | New lived scene — widen |
| Surrender to the Universe | 16s | Let go / surrender | **keep** | Wisdom bit — widen to clear resolve + 50s later |

Lesson: Opus surfaces leftover gold the instruction file missed. Our craft (entity + situation_resolve + 50s floor + script-first) still decides what ships.

## Does not

- Replace [`situation_resolve`](../situation_resolve/SKILL.md) or [`extract_shorts`](../extract_shorts/SKILL.md)
- Write `segments[]` or encode video
- Invent dialogue or polish into "better" prose
- Adopt external auto-titles, captions, or crops as the deliverable
- Plan 11–15 min chunks (that's [`chunks`](../chunks/SKILL.md))
- Run viral captions / sounds (step-2 `viral_captions` / `viral_sounds`)
