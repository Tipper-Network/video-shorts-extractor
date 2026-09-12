# Skill: Sound Effect Allocation

## Objective
Detect keyword triggers in word-level transcripts and overlay sound effects at precise timestamps.

## Input Requirements
- Source video path
- Word-level transcript JSON (`*.words.json`) from Vosk — fields: `word`, `start`, `end`
- Trigger config: `content_pipeline/sfx_triggers.json`

## Resolution Strategy (no local asset library)

SFX are resolved on demand via `content_pipeline/sfx_resolver.py`:

1. **Cache hit** — `content_pipeline/.cache/sfx/`
2. **Freesound API** — if `FREESOUND_API_KEY` is set
3. **Pixabay Audio API** — if `PIXABAY_API_KEY` is set
4. **Synthetic fallback** — generated WAV (works offline, no keys needed)

## Rules & Principles

1. **Trigger Word Detection**: Match words against `sfx_triggers.json` keys.
2. **Audio Overlay Precision**: Align SFX start to the word's `start` timestamp.
3. **Volume Balancing**: Attenuate SFX to 40% (`SFX_VOLUME = 0.4`).
4. **Debounce / Cooldown**: Minimum 0.8s between triggered SFX.

## Execution

```bash
# Word-level transcript (requires Vosk model)
python3 content_pipeline/process_stream.py --mode transcribe --input clip.mp4 --vosk

# Apply SFX + zoom
python3 content_pipeline/auto-edit.py \
  --input projects/my-video/output/master/timeline_normalized.mp4 \
  --output projects/my-video/output/master/timeline_polished.mp4 \
  --words projects/my-video/output/transcript/words.json
```

## Adding Triggers

Edit `content_pipeline/sfx_triggers.json`:

```json
{
  "money": { "query": "cash register coin", "synthetic": "cha_ching" }
}
```

- `query` — search term for Freesound/Pixabay
- `synthetic` — fallback generator type (`pop`, `ding`, `buzzer`, `cha_ching`, `whoosh`)
