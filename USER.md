# USER.md — Editing Preferences & Active Projects

Stable directives for content creation sessions. One directive per entry.

## Directives

<!-- observed: 2026-09-02 | status: active -->

- Git ships the **product others onboard on** (`skills/`, `planning/`, `content_pipeline/`, templates). Job folders, brand books, and this file stay local. Cursor+folders now; website UI later — same agents, same shorts/chunks.

<!-- observed: 2026-09-02 | status: active -->

- When planning storyline or editorial tone, read the named entity's file in `brands/` first. Tipper, THP, and GAF are siblings; do not collapse them. Founder spoken style (`USER.md`, Origin Story cuts) applies to all three.

<!-- observed: 2026-09-02 | status: active -->

- Prefer chronological ordering for multi-clip projects unless the narrative explicitly calls for reordering.

<!-- observed: 2026-09-02 | status: active -->

- Always consult `skills/entity_brand/`, then `skills/situation_resolve/`, then `skills/extract_shorts/`, `skills/vertical_shorts/`, `skills/chunks/` before making cut decisions. The video name picks the entity (Tipper / THP / GAF). A short that states a situation and does not resolve it fails. A resolved short that belongs to a different entity is leftover, not a ship.

<!-- observed: 2026-09-02 | status: active -->

- Never delete planning, skills, or instinct files — they encode the editing approach. Edit and refine instead.

<!-- observed: 2026-09-02 | status: active -->

- Keep project-specific edit requirements in `content_pipeline/projects/{name}/requirements.md` — never mix into platform skills/code.

<!-- observed: 2026-09-02 | status: active -->

- When a project reveals a platform gap, fix the skill/script first, then log it in `planning/capability-matrix.md`.

<!-- observed: 2026-09-02 | status: active -->

- For multi-clip assembly: **draft concat first** (fast stream-copy), review timeline, then normalize only if needed for export.

<!-- observed: 2026-09-02 | status: active -->

- **Outcome:** 2 types of deliverables: **Shorts** (9:16, up to 3 editorial versions) and **Chunks** (16:9, 11-15 min). Never render YouTube / TikTok / Reels copies of the same cut.
- Story-first usually wins when the elaboration is kept; put the punchline hook on the front of that cut. Level speech on the finished file (`level_speech`: compressor + dynaudnorm + limiter + loudnorm −16 / LRA 4) so live spikes don't jump.
- Agent must not go silent on long ffmpeg/transcribe jobs — background them and keep responding.
- Never overwrite a rendered clip the user can already play. Next pass writes `_v2`, `_v3`, … so both files stay for A/B. Only `--force` replaces in place. Never land on an existing `_vN`.
- Script before picture. Write the playback script to `deliverables/shorts/{stem}.md` (theme, problem, context, resolve + transcript lines). Wait for approval. Do not ffmpeg until the script is signed off. Draft mp4s stay in `shorts/`. Approved videos go to `deliverables/shorts_approved/`.
- Shorts duration: **50s floor, ~60s+ is the average.** Do not ship a speech short under 50s. Prefer 55–75s. Hard ceiling still 90s. Complete resolve still wins, but pad by holding the situation (more of the same thought), not by splicing a second story.
- Do not out mid-clause to dodge a pitch. If the land is “right now,” keep the finished example of the move.
- After the instruction-file themes are done, scan the leftover transcript. The brief is not a cap.

## Active Projects

<!-- observed: 2026-09-02 | status: active -->

- **Tipper The Story** (`projects/1. tipper the story/`) — active. Cut from `shorts_extraction.md`, not Gemini. Scripts + 9:16 drafts in `output/deliverables/shorts/`. Publish queue: sh05 → sh08 → sh03 → sh02 → sh06 → sh04 → sh01. Park sh07/sh09 (extracted, not promoted). Chunks not this pass.
- **Origin Story** — Approved: sh01 story-first (100s), sh02 island-bum hook-first (64s), sh03 focus-vs-tunnel hook-first (58s), sh05 moving-house first-stream close (44s). Draft: sh04 Game WITH Life (28s). Chunks: ch01, ch02. Deferred: ch03.
