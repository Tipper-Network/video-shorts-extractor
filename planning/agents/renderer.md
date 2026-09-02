# Agent: Renderer

**Role:** Batch-render all clips from an approved manifest using FFmpeg.

## Triggers

- Manifest approved (human or QA)
- User runs `--mode render`

## Inputs

- `content_pipeline/output/{stem}/manifest.json`
- Source video at path in manifest
- Platform constraints per clip entry (aspect, target prefix)

## Outputs

```
content_pipeline/output/{stem}/
  chapters/*.mp4
  shorts/*.mp4
  publish_queue.csv
```

## Skills

- [`skills/render-manifest/SKILL.md`](../../skills/render-manifest/SKILL.md)
- Platform skills (for aspect/duration reference only)

## Instincts

- [content-pipeline.md](../instincts/content-pipeline.md) — "Rendering" section

## Workflow

```
1. Validate manifest against schema
2. Create output subdirs (chapters/, shorts/)
3. For each chapter entry → ffmpeg cut 16:9
4. For each short entry → ffmpeg cut 9:16 with crop filter
5. Name files: {target}_{id}_{slug}.mp4
6. Write publish_queue.csv from manifest metadata
7. Log success/fail per clip; do not abort entire batch on single failure
```

## FFmpeg Reference (from process_stream.py)

- 16:9: `scale=1920:1080`
- 9:16: `crop=ih*(9/16):ih,scale=1080:1920`
- Codec: libx264 fast preset, aac audio

## Done When

- Every manifest entry has corresponding MP4 OR explicit error logged
- Filenames match manifest ids for traceability

## Does NOT

- Modify manifest timestamps
- Re-transcribe or plan clips (delegate to Cursor agent)
- auto-editor (Phase 6 — not yet)

## Future

- `--auto-editor-tightness` per platform (aggressive/moderate/light)
