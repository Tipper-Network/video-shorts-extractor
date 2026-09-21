---
name: situation-resolve
description: Makes a short's spoken script cohesive — name one situation (problem, issue, struggle, or intention), stay inside it, and do not out until it resolves. Use before cutting or splicing any speech short.
---

# Situation → Resolve

**This is the script skill.** [`extract_shorts`](../extract_shorts/SKILL.md) finds timestamps. This file decides whether those timestamps are *one thought that finishes*.

Read this before writing `segments[]`. Write the playback script to `deliverables/shorts/{stem}.md` and wait — do not ffmpeg to discover the argument.

## The rule

Take a situation and resolve it — whether it is a **problem**, **issue**, **struggle**, or **intention**.

One short = one situation. The viewer must hear:

1. **What it is** (the situation, in the world of this clip)
2. **What presses on it** (denial, cost, hinge — why it isn't already done)
3. **What changes** (the resolve)

If the audio never delivers (3), the ending is incomplete. If (2) is missing, the middle won't connect. If you swap to a second situation mid-splice, the script falls apart.

## Name it first

Write this in the manifest *before* picking extra windows:

```json
"situation": {
  "type": "problem",
  "statement": "I treat the 5% chance I'm the idiot as a joke and say no.",
  "pressure": "Of course I'm not — but what if I am; I could do better.",
  "resolve": "I stop reacting with no and give myself a chance to respond.",
  "resolved": true
}
```

| `type` | The situation is… | Resolve means… |
|--------|-------------------|----------------|
| `problem` | Something is broken or stuck | The move that unsticks it |
| `issue` | A distinction that isn't landing | The distinction is used, not just named |
| `struggle` | A lived bind (money, ego, identity) | A decision or exit from that bind |
| `intention` | A stated aim that hasn't been tested | Evidence they are living it — or changing it |

`statement`, `pressure`, and `resolve` must be quoteable from the transcript, not a paraphrase you wish he said.

## Hold the situation

Stay in the same situation until it resolves.

- Do not jump cafe-poverty into an island-bet unless a spoken line names the jump.
- Do not jump “you say no” into “chance to respond” if “I'm not / but what if I am” is the pressure — that hinge *is* the situation tightening.
- Elaboration is allowed (and usually required). Tangents are not. Handwriting, “sorry”, “let's do this” are deletes.
- Duration expands to fit the situation. **Shorts: 50s floor, prefer 55–75s.** Complete resolve wins. Hard ceiling 90s. Under 50s is a fail for this series.

**Chunks:** still one situation. The extra minutes are examples and elaboration of *that* situation, plus a structure the viewer can follow. Two jobs in one chapter fails the same way two situations in one short fail. See [`chunks`](../chunks/SKILL.md).

## Playback that holds

Story-first with the punchline on the front is the default when the situation needs room:

1. **Hook** — one line from *this* situation (question or punch). Same situation, not a teaser from another.
2. **Situation + pressure** — thorough elaboration. This is the body that made story-first win.
3. **Resolve** — the change, landed on a finished clause. Do not out on the setup of the insight.

`hook-first` without elaboration skips pressure. `contiguous` only if the take already contains situation + pressure + resolve. A contiguous window that only *tells the story* (no capture, no resolve) fails — Origin Story sh01 contiguous was this.

Do not stack two “but” hinges. sh01 story-first said “but what if” (~1:00) then “but I could” (~1:12). Cut the repeat (source `07:38–07:54`). One pressure turn.

## Spoken-as test

Paste the splice as one paragraph. It must read as:

> [situation]. [pressure]. [resolve].

Fail if:

- The paragraph changes situation without a spoken bridge
- Pressure is implied, not heard
- Resolve is named as a label (“reaction vs response”) but never happens in the audio
- The last sentence is still inside the situation (“I reacted with a no”) with no change
- You out mid-clause to avoid a pitch (“this is the first…”) — finish the example or don’t start the sentence
- “Right now” / “that’s the move” with no concrete instance (sh05 needed “this is the first stream”)
- A feedback loop is named as the closer (“revive that loop”) instead of the exit (“keep track”)
- The exit is named as an instruction (“you have to keep track”) with no spoken payoff of what that does
- The closer is a plot recap from a second situation (businesses-first, cafe sleep, GAF rant)
- You cannot point to a timestamp for `statement`, `pressure`, and `resolve`

## Origin Story — what failed, what held

**sh01 Reaction vs Response** — situation type: `problem` (ego says no).

| Cut | Why it broke / held |
|-----|---------------------|
| Question → you say no → list | No pressure. “I'm not / I am” never happens. Resolve is a label. |
| Same + duration knife at 09:40 | Situation never resolves. Closer is `10:04–10:08`. |
| Story-first + 5% hook on the front | Situation stated, pressure heard, respond closer lands. |

**sh03 Focus vs Tunnel** — situation type: `issue` (persistence becomes blindness).

| Cut | Why it broke / held |
|-----|---------------------|
| Tunnel hook → platform/money → businesses first | Recap. Resolve is a second story. Distinction never used. |
| Tunnel hook → no longer the thing / didn't work → question yourself or you revive the loop | Names the loop. Does not consolidate the method. |
| Detect → stop → question daily + keep track, out on “revive that loop” | Last sentence is still inside the loop. |
| Loop as pressure, land on “you have to keep track” | Names the exit. Does not resolve what keeping track *does*. |
| Keep track → write a note / capture the thought / different perspective | Practice completes. Skip “make a video.” |

**sh05 Moving House** — situation type: `struggle` (transition).

| Cut | Why it broke / held |
|-----|---------------------|
| `1:03:12–1:03:46` | Metaphor holds. Outs mid-clause on “this is the first…”. 34s — under floor. |
| `1:03:04–1:03:56` (breakup in) | Completes the videos. User preferred the first in-point. |
| `1:03:12–1:03:56` | Same in as the cut that worked. “First stream / the videos” = example of starting the move. Hard Port stays out. |

**sh02 Island Bum** — situation type: `intention` (own an island or live as a bum).

| Cut | Why it broke / held |
|-----|---------------------|
| Bet → cafe sleep | Two situations. “This is how I'm living” has no island. |
| Bet → boats/storm → close through `35:08` | Same intention, pressure (living the bum option), resolve (move / reconnect). |

## Does not

- Pick the theme (that's `shorts_instructions.md`)
- Pick 9:16 / write the file (that's `vertical_shorts`)
- Replace timestamp hunting (that's `extract_shorts` — it must pass *this* gate)
- Plan the 11–15 min chapter (that's `chunks` — still one situation; this file still gates the throughline)
