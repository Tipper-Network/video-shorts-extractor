---
name: edit-audio
description: Voice leveling on the step 1 cut, then step 2 stage 2 sounds. Use when checking loudness or SFX. Functions level_speech and cli/viral_sounds.py.
---

# Audio

Two passes. They do not duck a music bed. There is no music function.

## Voice — step 1, always

`level_speech` in `content_pipeline/lib/cut_utils.py` re-encodes audio on the finished cut. Video is copied.

`VOICE_AF`:

```text
acompressor=threshold=-24dB:ratio=8:attack=3:release=80:makeup=5
dynaudnorm=f=75:g=25:p=0.6:m=12
alimiter=limit=0.75:attack=3:release=30
loudnorm=I=-16:TP=-1.5:LRA=4
```

That is the noise control, the compression, and the loudness. There is no separate de-esser and no Audition session.

## Sounds — step 2, stage 2

Script: `content_pipeline/cli/viral_sounds.py`. Input is `viral/stage1/`. Output is `viral/stage2/`.

- A censor word from `content_pipeline/config/censor_words.json` is muted and replaced with a beep (`BEEP_VOLUME` 0.55). The caption already printed `****`.
- Other trigger words come from `sfx_triggers.json`. The hit is mixed at `SFX_VOLUME` 0.4. Next hit waits `SFX_COOLDOWN` 0.8s.
- Resolver order in `lib/sfx_resolver.py`: cache, then Freesound if a key exists, then Pixabay, then a synthetic wav.

`cli/auto_edit.py` is the old MoviePy path. It zooms every 4 seconds and layers the same SFX. Do not run it. Stage 2 is `viral_sounds.py` only.
