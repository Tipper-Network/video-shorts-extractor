---
name: extract-shorts
description: Planner rules for cutting speech shorts — locate a 3–5 min theme block, extract Hook / Setup / Resolution, splice, then fail any cut that is not a complete spoken statement.
---

# Extract Shorts

**Planner only. No ffmpeg.** Resolve the entity with [`entity_brand`](../entity_brand/SKILL.md) first (title = brand key). Themes come from `shorts_instructions.md` / `shorts_extraction.md`. Script cohesion is [`situation_resolve`](../situation_resolve/SKILL.md). Export stays in [`vertical_shorts`](../vertical_shorts/SKILL.md).

Read [`entity_brand`](../entity_brand/SKILL.md), then [`situation_resolve`](../situation_resolve/SKILL.md). Name the entity, then the situation. Then hunt timestamps.

**Origin Story lesson:** do not encode to find the argument. sh03 burned v2–v7 that way. Script `.md` first. Recap (businesses-first) is not a resolve. Last line inside a loop is not a resolve. “Keep track” without the payoff is not a finished resolve. Do not out mid-clause to dodge a pitch — if “right now” is the land, the next finished example of the move stays in (sh05: first stream). Never ship under 50s.

## Extraction Protocol

1. Identify the full 3–5 minute thematic block.
2. Extract:
   - [Hook Line]: The most memorable punchline or question.
   - [Core Setup]: 10–15s explaining the problem.
   - [Resolution]: 15–20s delivering the actionable insight.
3. Splice Hook -> Setup -> Resolution.
4. Verify that the spliced audio forms a 100% grammatically complete and logically coherent statement without missing context.

The 3–5 min block is the **search window**, not the cut. **50s floor. Prefer 55–75s (this series averages ~1 min).** Do not ship under 50s. Complete resolve still wins. Hard ceiling 90s. If the take is 30s, hold the same situation longer — do not splice a second story to pad.

## Modes / three editorial versions

Not platforms. Try all three on the same theme block. Keep only versions that pass the gate.

| `version_id` | `extract_mode` | Playback order |
|--------------|----------------|----------------|
| `hook-first` | `splice` | Hook → Setup → Resolution |
| `story-first` | `splice` | Setup → Hook → Resolution |
| `contiguous` | `contiguous` | One window if all three beats already sit in a clean **50–75s** take |

Hook may come from later in the block (`hook_source: later`). Do not force a splice when `contiguous` already holds.

## Workflow

0. Resolve `entity` from the video/folder name per [`entity_brand`](../entity_brand/SKILL.md). Read that entity's brand records. Write `entity` on `requirements.md`.
1. Read the theme from `shorts_instructions.md` / `shorts_extraction.md` (title, idea, candidate neighborhood).
2. Write `situation` (`type`, `statement`, `pressure`, `resolve`) per [`situation_resolve`](../situation_resolve/SKILL.md).
3. Open `output/transcript/transcript.txt`. Find the 3–5 min block by **spoken content**, not by the brief's timestamps if they disagree.
4. Quote the beats with `start` / `end` / `text` — include pressure/hinge and the resolve closer, not just hook + setup.
5. Paste into `coherence.spoken_as`. It must read [situation]. [pressure]. [resolve].
6. Run the gate below *and* the situation-resolve test. Fail = do not write `segments[]`. Do not render.
7. **Brand pass.** Keep / demote / park against [`entity_brand`](../entity_brand/SKILL.md). A finished thought that belongs to another entity is leftover, not a ship.
8. On pass, write labeled `segments[]` **and** a script file next to the draft videos:
   `output/deliverables/shorts/{id}_{slug}_{version}.md`
   Theme, problem, context, resolve, then the playback script (actual transcript lines + clocks, in splice order).
9. **Stop.** The user reads that file and tests the argument on paper. Do not ffmpeg until they approve the script (`script_approved: true`).
10. Draft renders stay in `deliverables/shorts/`. After the user signs off the *video*, copy it to `deliverables/shorts_approved/` (`--promote`). Do not render into that folder.
11. **After the instruction-file themes are scripted, scan the rest of the transcript.** The brief is a starting list, not a cap. Any leftover 3–5 min block that names a situation and resolves it is a candidate. Write it as a new `shNN` (or a leftover table) — do not silently drop it. Do not glue two leftover situations onto an existing short to “use the line.”

## Coherence gate (hard fail)

Reject if any of these are true:

- Pronoun with no antecedent in the splice (`that`, `this`, `these`, `it`, `she`, `they`)
- Answer without the question that makes it land
- Cut mid-clause (ends on "so when I realized that I…" or "this is the first…")
- The metaphor lands on "right now" / "that's the move" with no example of what right now *is* (sh05: keep "this is the first stream")
- Duration under 50s
- Setup restates the hook instead of stating the problem
- Resolution restates the hook instead of delivering the insight
- Resolution needs a whiteboard list, earlier story, or name the viewer never heard
- Brief timestamps land on handwriting, "sorry", "let's do this", or dead air — those are hard deletes, not beats
- Punchline is clipped mid-sentence (search until the clause lands)
- Denial and admission both appear (`I'm not` / `but what if I am`) but the spoken turn between them is missing
- Resolution names a framework (react vs respond) but never delivers the closer that uses it
- `situation.resolved` would be false — the splice states a problem/issue/struggle/intention and never changes it

## Manifest fields

```json
{
  "id": "sh01",
  "extract_mode": "splice",
  "theme_block": { "start": 350, "end": 588 },
  "hook": { "start": 366, "end": 378, "text": "What if there's a 5% chance I am an idiot?" },
  "setup": { "start": 390, "end": 406, "text": "First thing you do is no. …" },
  "resolution": { "start": 556, "end": 580, "text": "What I did was I reacted with a no. …" },
  "coherence": {
    "spoken_as": "What if there's a 5% chance I am an idiot? First thing you do is no. … All of these are me giving myself a chance to respond.",
    "complete": true
  },
  "cut_mode": "supercut",
  "segments": [
    { "start": 366, "end": 378, "label": "hook" },
    { "start": 390, "end": 406, "label": "setup" },
    { "start": 556, "end": 580, "label": "resolution" }
  ]
}
```

`segments[]` is what `render_manifest.py` cuts. The labeled beats + `spoken_as` are the planner contract.

## Worked example — Origin Story `sh01`

Theme: Reaction vs Response. Brief said Clip B was `07:15–08:05`. Transcript there is handwriting. Real distinction is `08:48–09:40`.

| Beat | Clock | Seconds | Why |
|------|-------|---------|-----|
| Theme block | 05:50–09:48 | 350–588 | Question through respond |
| Hook | 06:06–06:18 | 366–378 | Punchline lands at 06:18, not 06:12 |
| Setup | 06:30–06:46 | 390–406 | Denial is the problem |
| Resolution | 09:16–09:40 | 556–580 | List is the antecedent of "all of these" |

Failed splice: resolution `08:48–09:04` + closer without the list → "all of these" has no object.

v2 failed: jumped `06:06` question → `06:30` denial → `09:16` list. Missing `07:34–08:02` (*I'm an idiot, of course I'm not. But what if. I could do better.*) and missing closer `10:04–10:08`. Duration knife cut the topic in half.

## Worked example — Origin Story `sh02` (Island Bum)

Same theme, three versions. v1 failed because hook (childhood bet) jumped to cafe poverty — "this is how I'm living" had no island in the splice. Close was cut at `34:56` before "move forward / reconnect".

| Version | Order | Setup window | Why |
|---------|-------|--------------|-----|
| hook-first | bet → boats/storm → close | `32:32–32:48` | "This is how I'm living" = the island lifestyle |
| story-first | broke → bet → close | `31:08–31:24` | Chronology: exposed → I had named this life → I was living it |
| contiguous | `34:32–35:08` only | — | Payoff is already a complete statement |

Shared close: `34:32–35:08` (land on "better version of this life"). Do not mix two locations in one splice unless a spoken line names the jump.

**Version rule:** change order and which setup window. Do not render the same splice three times.

## Does not

- Invent a theme the transcript doesn't support (themes live in `shorts_instructions.md`; leftover scan *adds* to that file)
- Set 9:16 / write the file (that's `vertical_shorts`)
- Plan 11–15 min chunks (that's `chunks`)
- Render
