# Skill: Sound Effect Allocation

## Objective
Detect keyword triggers in word-level transcripts and overlay sound effects at precise timestamps.

## Input Requirements
- Source video path
- Word-level transcript JSON (`*.words.json`) from Vosk — fields: `word`, `start`, `end`
- Trigger config: `content_pipeline/config/sfx_triggers.json`

## Resolution Strategy (no local asset library)

SFX are resolved on demand via `content_pipeline/lib/sfx_resolver.py`:

1. **Cache hit** — `content_pipeline/.cache/sfx/`
2. **Freesound API** — if `FREESOUND_API_KEY` is set
3. **Pixabay Audio API** — if `PIXABAY_API_KEY` is set
4. **Synthetic fallback** — generated WAV (works offline, no keys needed)

## Live path

Step 2 stage 2. Input is `viral/stage1/`. Output is `viral/stage2/`. A trigger does not choose the short.

```bash
python3 content_pipeline/cli/viral_sounds.py
```

Censor words mute and beep (`BEEP_VOLUME` 0.55) so the sound matches the `****` from stage 1. `--land` is the only other hit, and only if that word is also in `sfx_triggers.json`. Volume 0.4, cooldown 0.8s.

Do not run `content_pipeline/cli/auto_edit.py`. It still zooms every 4 seconds. Zoom is cancelled.

## Rules & Principles

1. **Trigger Word Detection**: Match words against `sfx_triggers.json` keys.
2. **Audio Overlay Precision**: Align SFX start to the word's `start` timestamp.
3. **Volume Balancing**: Attenuate SFX to 40% (`SFX_VOLUME = 0.4`).
4. **Debounce / Cooldown**: Minimum 0.8s between triggered SFX.

## Adding Triggers

Edit `content_pipeline/config/sfx_triggers.json`:

```json
{
  "money": { "query": "cash register coin", "synthetic": "cha_ching" }
}
```

- `query` — search term for Freesound/Pixabay
- `synthetic` — fallback generator type (`pop`, `ding`, `buzzer`, `cha_ching`, `whoosh`)
