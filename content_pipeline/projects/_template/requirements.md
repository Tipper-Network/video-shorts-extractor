# {Project Name} — Requirements

> Copy this file to `projects/{name}/requirements.md` and fill in.  
> Platform capabilities: [`planning/capability-matrix.md`](../../planning/capability-matrix.md)

## Identity

| Field | Value |
|-------|-------|
| Project ID | `{name}` |
| Series JSON | `content_pipeline/series/{name}.json` |
| Source folder | `~/Desktop/{name}-project/` |
| Output folder | `content_pipeline/output/{name}/` |

## Goal

> One paragraph: what is this video when it's done?

## Audience & outputs

- **Audience:**
- **Primary output:** (e.g. one 16:9 timeline / shorts / both)
- **Target length:**

## Source assets

| Rule | Value |
|------|-------|
| Sort order | (e.g. filename timestamp) |
| Exclude files | |
| Include stills? | yes / no |
| Still placement | (if yes: where?) |

## Edit requirements

### Assembly
- [ ] Chronological concat
- [ ] Normalize portrait / missing audio
- [ ] Insert stills

### Pacing
- [ ] Silence trim threshold: (e.g. gaps > 3s)
- [ ] Remove filler words: yes / no

### Visual
- [ ] Reframe to 9:16 for shorts
- [ ] Subtitles: off / burned-in / SRT
- [ ] Dynamic zoom: yes / no

### Audio
- [ ] SFX on trigger words: yes / no
- [ ] Background music: none / genre

## Clips to cut

List filenames or timestamps to remove entirely:

-

## Known issues

| Issue | Location | Status |
|-------|----------|--------|
| | | open / fixed |

## Decisions log

| Date | Decision | Notes |
|------|----------|-------|
| | | |

## Platform capabilities used

Check capabilities exercised — update matrix after each run:

- [ ] `concat_clips` — chronological assembly
- [ ] `concat_clips --mode normalize`
- [ ] `concat_clips --include-images`
- [ ] `process_stream --mode transcribe`
- [ ] `render_manifest`
- [ ] `auto-edit` (SFX + zoom)
- [ ] Cursor agent manifest planning

## Status

| Step | Status | Artifact |
|------|--------|----------|
| Assembly | | |
| Transcript | | |
| Edit plan | | |
| Polish | | |
| Final export | | |
