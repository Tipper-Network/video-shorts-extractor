---
name: vertical-shorts
description: Rules for 9:16 vertical shorts — one cut per editorial version, written to deliverables/shorts/.
version: "2.0.0"
---

# Vertical Shorts

**Two deliverable types only:** shorts (9:16) and chunks (16:9). This skill is export + canvas. Cut logic is [`extract_shorts`](../extract_shorts/SKILL.md).

One short concept → one file, unless the planner kept more than one **editorial version**. Never fan out to YouTube / TikTok / Reels.

## Content Goal

High-value vertical snippets. Same file is the short — platform upload is a publish step, not a render step.

## Shared Planning Rules

- **Aspect ratio:** 9:16 (1080×1920)
- **Visual Reframe:** Shrink 16:9 video to fit frame width (1080); stack over blurred vertical background (avoid side-cropping).
- **Cut modes:** `contiguous` (single window) or `supercut` (`segments[]` montage)
- **Audio:** After the picture is cut, `level_speech()` always re-encodes audio: compressor + `dynaudnorm` + limiter + `loudnorm` (−16 LUFS, LRA 4). First pass on concat was too soft and still spiked.
- **Captions:** Kinetic subtitles on polish pass
- **Flywheel:** Tag each short with `flywheel_stage`; set `publish_order`

## Three editorial versions (not platforms)

When extracting, try all three. Keep only versions that pass the [`extract_shorts`](../extract_shorts/SKILL.md) coherence gate.

| `version_id` | Approach | Order |
|--------------|----------|-------|
| `hook-first` | Punchline / question first | Hook → Setup → Resolution |
| `story-first` | Problem first, punch later | Setup → Hook → Resolution |
| `contiguous` | All three beats already in one take | Single window — do not splice |

Render: `{id}_{slug}.mp4` if one version; `{id}_{slug}_{version_id}.mp4` if more than one survived.

Duration target **50–75s** (series average ~1 min). Floor 50s. Hard ceiling 90s. One trim profile on the short (`moderate` default) — not per platform.

## Manifest Shape

```json
{
  "deliverables": {
    "shorts": { "skill": "skills/vertical_shorts" },
    "chunks": { "skill": "skills/chunks" }
  },
  "shorts": [
    {
      "id": "sh01",
      "title": "Reaction vs Response",
      "cut_mode": "supercut",
      "aspect": "9:16",
      "extract_mode": "splice",
      "version_id": "hook-first",
      "segments": [
        { "start": 366, "end": 378, "label": "hook" },
        { "start": 390, "end": 406, "label": "setup" },
        { "start": 556, "end": 580, "label": "resolution" }
      ]
    }
  ]
}
```

Optional `versions[]` on one short when two or three approaches passed:

```json
"versions": [
  { "version_id": "hook-first", "cut_mode": "supercut", "segments": [] },
  { "version_id": "story-first", "cut_mode": "supercut", "segments": [] }
]
```

## Render

```bash
python3 content_pipeline/render_manifest.py \
  --manifest "projects/{name}/output/plan/manifest.json" \
  --project {project_id} \
  --type shorts
```

Output:
- Script (before picture): `deliverables/shorts/{id}_{slug}_{version}.md`
- Draft render: `deliverables/shorts/{id}_{slug}_{version}.mp4`
- Signed-off video: `deliverables/shorts_approved/` (copy via `--promote`, never render straight in)

## Agent Checklist

1. Read `shorts_instructions.md` for themes
2. Name the situation with [`situation_resolve`](../situation_resolve/SKILL.md), then cut with [`extract_shorts`](../extract_shorts/SKILL.md) — try hook-first, story-first, contiguous
3. Validate timestamps against `output/transcript/transcript.txt`
4. Write the script `.md` in `deliverables/shorts/` and wait for approval
5. Write **one** short entry per concept (plus `versions[]` only if more than one approach passed)
6. Pair with [`chunks`](../chunks/SKILL.md) for 11–15 min mid-form
7. Promote signed-off mp4s to `deliverables/shorts_approved/`

## Deprecated

Platform fan-out is dead. Do not set `platforms: ["youtube", "tiktok", "reels"]`. Do not write `_youtube.mp4` / `_tiktok.mp4` / `_reels.mp4`.
