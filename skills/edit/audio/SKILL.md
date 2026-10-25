---
name: edit-audio
description: Voice leveling on the step 1 cut, then step 2 stage 2 sounds. Use when checking loudness or SFX. Functions level_speech and cli/viral_sounds.py.
---

# Audio

Two passes. They do not duck a music bed. There is no music function.

## Voice — step 1, always

`level_speech` in `content_pipeline/lib/cut_utils.py` re-encodes audio on the finished cut. Video is copied.

`voice_chain()` runs in this order, then the same loudness on every file:

```text
deesser
equalizer 220 Hz +2.5 dB, equalizer 3200 Hz +3 dB
loudnorm=I=-16:TP=-1.5:LRA=11
```

`afftdn` is added in front of that chain only when the manifest entry sets `room_tone: true`.

Do not put a compressor, a limiter, or `dynaudnorm` back in front of `loudnorm`. On lecture 13 the 75 ms gain rider plus LRA 4 lifted the gap between words and the file sounded cut. The choice on 2026-10-26 is loudness only: −16 LUFS, true peak −1.5, LRA 11. The de-esser and the two presence bands stay.

`auto-editor`'s bundled binary does not start on glibc 2.35. Do not replace its 0.6 s margin with `silenceremove` at peak −40 dB. That pass chops inside words. Lecture 13 shorts were recut with trim off. Chunks may still use the 2.5 s light profile.

## Sounds — step 2, stage 2

Script: `content_pipeline/cli/viral_sounds.py`. Input is `viral/stage1/`. Output is `viral/stage2/`.

- A censor word from `content_pipeline/config/censor_words.json` is muted and replaced with a beep (`BEEP_VOLUME` 0.55). The caption already printed `****`.
- A hit from `sfx_triggers.json` plays only when the word is the script's land (`--land`, the Resolve line). Volume 0.4. Cooldown 0.8s. Every other trigger key stays silent.
- Resolver order in `lib/sfx_resolver.py`: cache, then Freesound if a key exists, then Pixabay, then a synthetic wav.

`cli/auto_edit.py` is the old MoviePy path. It zooms every 4 seconds and layers the same SFX. Do not run it. Stage 2 is `viral_sounds.py` only.
