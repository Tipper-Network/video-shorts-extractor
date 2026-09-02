# Agent: Transcriber

**Role:** Extract audio and produce a complete timestamped transcript. Foundation for all downstream planning.

## Triggers

- Orchestrator requests transcription
- Transcript missing or stale vs input video mtime

## Inputs

- `content_pipeline/input/{filename}.mp4`

## Outputs

- `content_pipeline/audio/{stem}.wav` (16kHz mono)
- `content_pipeline/subtitles/{stem}.json` (segment array)

## Segment Format

```json
{"start": 0.0, "end": 4.2, "text": "segment text"}
```

## Skills

- Execution via `content_pipeline/process_stream.py` extract+transcribe functions (or dedicated module when split)
- No platform skills

## Instincts

- [content-pipeline.md](../instincts/content-pipeline.md) — "Transcription" section

## Workflow

```
1. Confirm input exists
2. ffmpeg extract → audio/{stem}.wav
3. Faster-Whisper transcribe FULL file (no segment cap)
4. Write subtitles/{stem}.json
5. Log segment count and duration coverage
```

## Done When

- JSON covers full video duration (last segment end ≈ video length)
- Base filename matches across input/audio/subtitles

## Does NOT

- Truncate transcript for LLM convenience
- Plan chapters or shorts
- Call external LLM APIs (planning is Cursor agent's job in-session)
