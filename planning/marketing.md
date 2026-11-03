# Marketing, psychology, and themes

Future strategies are written against this page. The two products already named — an ordered shorts queue, and a chapter with shorts around it — stay in [`flywheel-strategies.md`](flywheel-strategies.md). This page is the layer under them: the state a person is in, the chance one file gives them, and what a later strategy is allowed to choose.

A cut is chosen in this order. Brand, then stage, then theme, then the situation, then the clocks.

| Name | The question it answers | Written as |
|------|-------------------------|------------|
| Brand | Whose film this thought belongs to | `entity`, from the folder name. Books live in `brands/`. |
| Stage | Which move this file makes in the viewer's mind | `flywheel_stage` |
| Theme | The chance this one file gives the audience | `theme` on the script, before the clocks |
| Situation | The thought that has to finish inside the file | statement, pressure, resolve |

The 3–5 minute block in the transcript is the search window (`theme_block`). It is where you hunt. It is not the theme of the short.

## Psychology

Each stage is a state the viewer is in when the file ends. One file does one state. The same state can repeat when the chance is new. A state the tape does not contain is skipped. A file invented to fill an empty state is a feeling nobody earned.

| Stage | They leave feeling | The file has to | It fails when |
|-------|--------------------|-----------------|---------------|
| attract | "This is about me." | A stranger hears one contradiction and knows what the film is. Out on that line. | It announces a series, or teaches a method. |
| engage | "I want to respond." | They can answer it in their own room tonight. One story, one land. | The same land is reused on another file. |
| trust | "This person is real." | He is specific about himself. The lesson can wait. Several of these can sit on one lecture. | The same sentence is the land of a second short. |
| service | "That helped me." | One job they can do. On an episode, this is the 11–15 min chapter. On a shorts queue, this is a short taste of the job. | A 70-second clip is labeled service on an episode. |
| referral | "Others got results too." | Someone else's result. | His own mistake is relabeled as proof. A collage is built to fill the slot. |
| loop | "I need to see what is next." | The smallest action, then the gap between the inside and what the world hears. | A diagram he did not finish. |

Publish order follows the states when the tape has them: attract, engage, and trust before the chapter; referral and loop after. Skip a state that was not cut.

Register is part of the psychology. The viewer has to stay inside one felt situation until it lands. A confession and a later syllabus are two chances, so they are two files. An illustration that changes the vibe is not the missing context for the file in front of it. Lecture 13: making versus taking stays on 13-sh02 (02:27–03:21). The clarity list is 13-sh12 (05:06–06:00). Mom is the example inside 13-sh13 (11:01–12:04), whose land is "the decision is taken from the environment."

One land sentence per file. Two files that land on the same sentence are one short.

## Themes

Three different things share the word. Keep them apart when a strategy is written.

**The short's theme** is the chance that file gives. It is named before the clocks. Lecture 13, 13-sh02: the chance to consider making a decision against taking one. He names the pair and stops. The definition of the pair is a different chance, on 13-sh13: the room already took the decision, and mom is the example. Both files are engage. The stage repeats because the chance changed.

**The series subject** is what the episode keeps returning to, including the chapter title. Shorts on one episode can share a subject and still each carry their own chance. "Continue the theme" means the subject. It does not mean every short offers the same chance.

**The search window** is the 3–5 minutes of tape you read to find the chance. It is not shipped. The shipped file is 50–75 seconds, floor 50, ceiling 90, and it finishes the situation.

A theme the transcript does not support is not a theme. Leftover scan adds chances the brief missed. It does not invent a chance to fill a stage.

## Marketing

Marketing here is the journey of those states, in public, on a named brand.

Two strategies already exist. They use the same six states and reach a different conclusion.

| | flywheel-shorts | flywheel-episode |
|--|-----------------|------------------|
| Hero | The ordered shorts are the product. | The chapter is the product. |
| Where service lives | A short taste of the job. | The 11–15 min chapter. |
| What the viewer concludes | Trust built by the sequence itself. | Shorts, then the full job in the chapter, then the loop. |
| Long tape | A mine. Publishing it whole is optional. | The chapter. |

Pick one per project. The same source can produce two manifests when both conclusions are wanted. Future Ready is flywheel-episode: the two chapters are the service.

Brand is the queue. Tipper, THP, and GAF do not share a vocabulary on one file. A finished thought that belongs to a sibling is leftover on this title. Founder spoken style stays on all three. A file does not close on a sibling's product.

The live pipe is not a strategy. One video per weekday, Asia/Beirut, and only a row marked `scheduled`. `content_pillar` on the Sheet is the old weekday map. The slot is filled by `flywheel_stage`. The pipe posts. It does not choose the cut.

## The pair — scheduled cut, then a live

<!-- added: 2026-10-26 | reason: connection is a live after the prescheduled lecture short -->

Posts cut from a long video can take a pair.

1. **The scheduled file.** One post from the long tape, already cut, already on the weekday queue. It carries the stage and the theme. On a post like 13-sh02, the audience gets the chance to consider making a decision against taking one.
2. **The live, right after.** He goes on and discusses that post: elaborates, reflects, stays with the people who just saw it. This is the connection. He does it. The cron does not post it, and it is not a second row on the Sheet.

The live is its own piece. It reflects on the scheduled file. It is not a recut, not a second land spliced onto the short, and not a fill for a flywheel stage the tape skipped. The weekday queue stays one scheduled video per date. The live sits beside that date, in his hands, after the post is up.

## What a future strategy has to say

A new strategy is a section in [`flywheel-strategies.md`](flywheel-strategies.md) plus a playbook JSON. It keeps these six states. It does not add a seventh name for the same feeling.

It has to name:

1. The hero product, and which act holds service.
2. The audience's home: a short feed, or a long sit.
3. Which states it is allowed to skip when the tape has none.
4. The series subject, and the rule that each file still gets its own chance.
5. The brand whose queue the files join.

It inherits the cuts that are already law: one stage, one theme, one land, sentence edges, 50–75 seconds on a short, 11–15 minutes on a chapter, script signed before ffmpeg.

Still open, on purpose:

- The posting-strategy skill is not in force. [`quota`](../skills/quota/SKILL.md) is a draft. [`publish_schedule`](../skills/publish_schedule/SKILL.md) is the pipe.
- Series state (`series.theme`, episode, last stage) is planned in [`flywheel_series`](../skills/flywheel_series/SKILL.md). It does not run yet.
- A bad cut is fixed by a dated line in [`instincts/content-pipeline.md`](instincts/content-pipeline.md) or the skill it belongs to. Analytics, when they exist, do not gate the cut.
- Every lecture 13 short now has its chance named on the script. 13-sh03 through 13-sh11 were recut 2026-10-26 from the lecture with loudness only, because the earlier pass still had the compressor.
- The website will call this same manifest. It does not get a second cut language.
