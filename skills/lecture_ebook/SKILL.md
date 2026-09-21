---
name: lecture-ebook
description: Turns linearized GAF lecture transcripts (plain.txt from YouTube .srt) into a field book. Use when the user asks for an ebook, book, or chapters from Program Future Ready / GAF lectures — not for shorts or ffmpeg.
---

# Lecture → Ebook

Planner only. No ffmpeg. Source is `{n}. {Title}.txt` in `output/transcript/` (plain, no clocks). Clocked cuts live in each lecture folder as the same filename.

Read [`entity_brand`](../entity_brand/SKILL.md) first. This job is **GAF**. Then [`GAF_Brand_Brief.md`](../../brands/GAF_Brand_Brief.md) and [`GAF_Brand_Book_Updated.md`](../../brands/GAF_Brand_Book_Updated.md). Founder spoken style stays (`USER.md`). Tipper and THP stay out of the closer.

Drop list, chapter map, and vocab: [`reference.md`](reference.md).

## What this is

A **field book**, not a transcript dump and not a school. The lectures are live whiteboard + Twitch. The book is the thought after the glitch.

Positioning (do not paraphrase into hustle):

> The G.A.F. is where people bring their own frontier — not to be taught, but to be guided.

Pillar: **assumptions, not lack of effort, slow people down.** Questions beat slogans.

## Workflow

1. Resolve entity = GAF. Write it on `requirements.md`.
2. Read `{n}. {Title}.txt` in `output/transcript/` for every lecture in the series (order 13→18). Do not invent a seventh lecture.
3. For each lecture, name **one spine** (situation → pressure → resolve) the way [`situation_resolve`](../situation_resolve/SKILL.md) names a short — then keep the chapter inside it.
4. Cut stream wreckage (see reference). Keep the example that proves the move (house/phone, tree, water tank, control vs charge).
5. Write **two** files (lecture order, same spines):
   - `output/ebook/Future-Ready.md` — **full book**. Every kept argument and example from the titled plains in `output/transcript/`. ~2,500–4,500 words per chapter. Complete, not a pamphlet.
   - `output/ebook/Future-Ready-Summary.md` — **summary ebook**. Standalone. **≥30 trade pages** (count **300 words/page** → **≥9,000 words**). Same six chapters, compressed. Still has the proofs (house, tree/Ford, tank, control/charge, month, duty). Not a bullet outline.
6. Front matter on both: how to read, the six questions, what this is not.
7. Brand pass: GAF hall language. No hustle, no pitch-deck, no Tipper as the ending. Sister software may be named once as infrastructure, then dropped.
8. Stop. User A/Bs. Do not “finish” into KDP formatting unless asked.

## Voice

Calm, precise, conversational. Play as method. Shackleton-honest. Prefer: explore, map, notice, question, test, guide, frontier.

Banned on the page: hustle, grind, unlock, leverage, empower, growth-hack, crush, dominate.

Do not write like a course. Do not write like a memoir that never lands the idea. First person is allowed when it is *his* proof (folding clothes, walking, Africa water, recycling). Do not invent scenes he did not tell.

## Chapter shape

```markdown
# {Lecture title}

{Opening question or distinction — one or two sentences.}

{The situation in the world of this lecture.}

{The example that makes it physical.}

{The resolve — what changes in how you look.}

{The six questions only if this chapter actually uses them.}
```

Target: two products. **Full** = complete lecture thought, 2,500–4,500 words/chapter. **Summary** = ≥9,000 words (≥30 pages at 300 wpp). Titled plains in `output/transcript/` are source. Do not pad reconnects; do not ship a 4k spine as the full book.

## Does not

- Replace the titled plains in `output/transcript/` (keep the raw)
- Overwrite Whisper clocks on lecture 13 (`13. Future Ready, The Program.txt`)
- End a GAF chapter on Tipper donations, the app, or “apply now”
- Mix THP nautical / Tipper “one tip” copy into body prose
- Keep `[ __ ]`, “uh”, “cool beans”, chat shout-outs, whiteboard fights
