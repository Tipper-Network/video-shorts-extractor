# Instincts: Content Pipeline (All Agents)

## Transcription

<!-- added: 2026-09-01 | reason: 150-segment cap loses 2hr content -->
- **Never** truncate the transcript before planning. The full JSON is the source of truth.
- **Always** verify last segment timestamp ≈ video duration before handing off to planners.
- **Always** keep matching base filenames across input / audio / subtitles.

## Chapter Boundaries

<!-- added: 2026-09-01 | reason: youtube-chunks skill requirements -->
- **Never** cut mid-sentence or mid-explanation.
- **Always** include ~10 seconds of context before a topic's main point starts.
- **Prefer** ending at natural topic transitions over hitting exact duration targets.
- **Never** produce a chapter shorter than 600s without flagging it for human review.
- **Never** produce a chapter longer than 1800s without splitting or flagging.

## Entity (title = brand)

<!-- added: 2026-09-21 | reason: Tipper / THP / GAF are named on the video -->
- **Always** resolve entity from the video/folder name before extracting (`skills/entity_brand`).
- **Always** read `brands/` for that entity (`Tipper_Brand_Book.md` / `the-hard-port-brief.md` / GAF brief+book). Desktop copies are fallback only.
- **Never** apply THP observational series rules to a Tipper-titled video, or GAF guild copy to a THP video.
- **Always** apply founder spoken style (`THP-MEDIA-003` Founder Narration + situation_resolve) on every entity.
- **Prefer** parking a finished thought that belongs to a sibling entity over shipping it on the wrong queue.

## Flywheel

<!-- added: 2026-09-01 | reason: user flywheel strategy -->
- **Always** tag every short with exactly one flywheel stage.
- **Never** let a short fully replace its parent chapter — shorts tease, chapters deliver.
- **Prefer** sequencing shorts attract → engage → trust → service before publishing the chapter, then referral → loop after.
- **Always** write a CTA that points toward the parent chapter or next episode for attract, service, and loop stages.
- **Prefer** continuing the same theme across an episode's shorts and its chapter title.

## Rendering

<!-- added: 2026-09-01 | reason: batch render reliability -->
- **Never** re-transcribe during render — manifest timestamps are frozen at approval.
- **Always** validate manifest against schema before first ffmpeg call.
- **Prefer** logging per-clip failures over aborting the entire batch.
- **Never** overwrite an existing rendered clip. Write `{stem}_v2.mp4`, `_v3`, … so the previous file stays for A/B. `--force` only when the user explicitly asks to replace. Never ffmpeg `-y` onto an existing `_vN`.
- **Never** out mid-clause to dodge a pitch. If the land is “right now,” keep the finished example of the move (sh05: “this is the first stream”).
- Shorts floor 50s, prefer ~60s+. Do not ship 28–34s WisdomBits.
- **Never** ffmpeg a recut until the user has approved the playback script in `deliverables/shorts/{stem}.md`. Script first, picture second.
- Draft mp4s stay in `deliverables/shorts/`. Signed-off videos are copied to `deliverables/shorts_approved/`.

## Local-First

<!-- added: 2026-09-01 | reason: workspace architecture -->
<!-- updated: 2026-09-02 | reason: Ollama removed; Cursor agent is planner -->
- **Prefer** local Whisper + FFmpeg over paid SaaS unless user explicitly approves spend.
- **Always** plan chapters and shorts via Cursor agent in-session — read full transcript, apply instincts, write manifest.
- **Never** exfiltrate raw video or transcripts to external APIs without user approval.

## Human Gate

<!-- added: 2026-09-01 | reason: plan-review-render decision -->
- **Always** pause for manifest review on first run of a new series.
- **Prefer** human review until QA Reviewer agent has 3+ consecutive PASS runs on a series.

## Assembly & Long Jobs

<!-- added: 2026-09-02 | reason: hikmat concat blocked chat for 7+ min -->
- **Always** use `content_pipeline/concat_clips.py` for chronological multi-clip assembly — not ad-hoc ffmpeg loops.
- **Prefer** `--mode draft` first (stream-copy, seconds) to review timeline order and pacing.
- **Only** use `--mode normalize` when portrait clips, missing audio, or export quality requires it.
- **Never** block the chat waiting on ffmpeg — background jobs expected >30s; report command, ETA, and output path immediately.
- **Prefer** `--preset ultrafast` for draft/normalize passes; reserve `medium`/`slow` for final export only.
- **Always** run `--dry-run` before a long normalize when clip count ≥5.
