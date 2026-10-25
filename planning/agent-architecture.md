# Video Editing Agent Architecture

How this workspace actually edits, judges, and posts. Skills say how. Instincts say what must not happen. The human signs the script before ffmpeg, and Dokploy posts after the Sheet says `scheduled`.

## 1. Skills

Map: [`skills/CATALOG.md`](../skills/CATALOG.md). Three organizations. They do not nest.

| Organization | Read when | Hub |
|--------------|-----------|-----|
| Brand | Whose queue this thought belongs to | [`entity_brand`](../skills/entity_brand/SKILL.md), `brands/` |
| Selection | What gets cut from the tape | [`situation_resolve`](../skills/situation_resolve/SKILL.md), [`extract_shorts`](../skills/extract_shorts/SKILL.md), [`chunks`](../skills/chunks/SKILL.md) |
| Posting strategies | Later. How signed videos take a slot | [`planning/flywheel-strategies.md`](flywheel-strategies.md). Draft: [`quota`](../skills/quota/SKILL.md). Live pipe: [`publish_schedule`](../skills/publish_schedule/SKILL.md) |

On a cut, read brand, then selection. Edit subcategories (retention, timeline, type, audio, package) run after the land is chosen. Do not read a posting strategy to decide which moment to keep.

Long-form work names one job. It does not score segments 0–100, and it does not invent a bridge with B-roll when the tape already holds the thought. Entry and exit are sentence edges, about 10 seconds of context before the point.

Short-form work is one 9:16 file, 50–75 seconds. The reframe fits the 16:9 picture to 1080 wide and stacks it on a blurred vertical ground. Captions are kinetic, `margin_v` 500, burned in. The first three seconds are the situation or its punchline, spoken, from this tape.

## 2. Instincts

Full text: [`planning/instincts/`](instincts/README.md). These are the operating rules, not a generic pacing table.

| Domain | Rule |
|--------|------|
| Entity | Resolve the brand from the folder name before any cut. Park a finished thought that belongs to a sibling. |
| Script | Write `deliverables/shorts/{stem}.md` and wait. No ffmpeg until that script is signed. |
| Speech | Do not cut mid-sentence. Shorts floor 50s. Chunks 11–15 min. Pad by holding the same thought. |
| Transcript | Plan from the YouTube `.srt` when it is the same file. Whisper only the locked window. Never re-transcribe a finished job. |
| Render | Never overwrite a file the user can play. Next pass is `_v2`. Draft concat first. |
| Publish | Only `scheduled` rows, Beirut date, one weekday post. Header stays on Sheet row 1. |
| Secrets | Refresh tokens live in the Dokploy API env. Not in git, not in the browser, not as a laptop path on the server. |

Pacing is platform-shaped only at the deliverable: shorts are tight speech, chunks keep a conversational sit. Silence trimming is not the editor. Brand color and a −18 dB duck are not house rules. Caption height, loudness (−16 LUFS, LRA 4), and the entity book are.

## 3. Feedback loop

```text
transcript + brand + instincts
        |
        v
script.md  -->  human sign-off  -->  manifest.json
        |
        v
ffmpeg render  -->  human plays the file  -->  _vN if it is wrong
        |
        v
S3 + Sheet status=scheduled  -->  Dokploy posts one row
        |
        v
correction written into instincts / USER.md / the skill
```

There is no exemplar XML library and no YouTube Analytics pull. A bad cut is fixed by a dated instinct line (`<!-- added: YYYY-MM-DD -->`) or a skill edit, then the next job reads it. Analytics, when we want them, are a later loop. They do not gate the cut.

The human gates are: which jobs are chapters, the playback script, and the Sheet status. The agent does not flip `scheduled` on its own. `ready` and `approved` stay parked.

## 4. How a stage finds the short

Every plan takes **as many shorts as the tape can hold**. The stage names the job. It is not a quota, and it is not a cap. One short does one stage. The same stage repeats for every new land. A stage that is not on the tape is skipped. Do not collage two stories to manufacture one more file. Do not stop because a tidy set already exists.

Future Ready is **flywheel-episode**. The chapter is the service. Shorts are everything else that resolves.

```text
name the service (one or more chunks)
        |
        v
attract, engage, trust        as many shorts as the tape holds
        |
        v
chapter(s)                    the job they can do tomorrow
        |
        v
referral, loop                only the posts the tape actually has
```

| Stage | What the cut has to do | What fails it |
|-------|------------------------|---------------|
| attract | A stranger hears one contradiction and knows what this film is. Out on that line. | A series announcement. A method. |
| engage | They can answer it in their own room tonight. One story, one land. | The same land reused on another short. |
| trust | He is specific about himself. Not the lesson. Several of these can sit on one lecture. | The same sentence used as the land of a second short. |
| service | The 11–15 min chunk. One job, two or three examples, then the land. | A 70s clip labeled service. |
| referral | Someone else's result. | His own mistake, relabeled. A collage built to fill the slot. |
| loop | The smallest action, then the gap between the inside and what the world hears. | A diagram he did not finish. |

Once the moment is the one that does the stage:

- In and out on sentence edges. About ten seconds of the same thought before the point.
- One land per short. The same land on two files is one short.
- 50–75 seconds. Eighty seconds means the out is late. A beat under 50s stays inside the short it already belongs to.
- A splice is two beats of the same situation. It is not a cut every three seconds.
- Zoom and sound effects run after the script is signed. They do not find the moment.
- No B-roll bridge, no crop tracker, no XML library. The 9:16 stack waits on a signed script.

## 5. Lecture 13 slate

Five of six stages are already named. No referral. This table is not the cap. After these outs are written, scan the rest of the lecture and keep every other land that clears the floor.

| Stage | Cuts | What |
|-------|------|------|
| attract | 2 | Who are we vs who we are (13-sh01, out on the difference, not "this is a series"). The million with no floor, only if 25:35–26:29 lands on its own above 50s. |
| engage | 1 | 13-sh02. Mom, the phone, one minute. That land is not used again. |
| trust | 3 | 13-sh03 comfort / the forgotten walk, without the mom land. 13-sh04 the France bus, re-clocked so it does not depend on the million open. 13-sh05 honest is the state. |
| service | 2 | 13-ch01 walk a real room. 13-ch02 when the goal has no corridor. The bus may also be an example inside ch02. |
| referral | 0 | Not on this tape. |
| loop | 1 | 13-sh06 French out loud. Under 75s. Scribble stays out. |

Scripts stay unsigned until those outs are written. No ffmpeg on this slate yet.
