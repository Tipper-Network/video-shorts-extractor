# Step 2 — Viral edit

Jobs land here **after** shorts + chunks are cut in [`../step-1-projects/`](../step-1-projects/). The whole job folder moves; do not leave a half-cut job here.

**Stage:** polish signed cuts into social-ready picture (captions, on-screen type, covers). Cut masters stay under `output/`. Viral end results go under **`viral/`** — never overwrite `output/`.

Queue + stage map: [`../step-1-projects/VIDEO-EDITS.md`](../step-1-projects/VIDEO-EDITS.md).

## Layout (every job)

```text
step-2-viral-edit/{name}/
├── input/                      ← source (moved with the job)
├── output/                     ← CUT ONLY — do not overwrite
│   ├── transcript/ plan/ logs/
│   └── deliverables/
│       ├── shorts/             ← letterbox masters
│       ├── shorts_approved/    ← signed cut scripts / mp4s
│       └── chunks/
└── viral/                      ← VIRAL EDIT END RESULTS
    ├── shorts/                 ← captions + on-screen type + polish
    ├── covers/                 ← 9:16 stills (one per short)
    └── approved/               ← signed viral packs → handoff to step-3
```

## Rules

1. **Read** cut masters from `output/deliverables/` (prefer `shorts_approved/` when present).
2. **Write** only under `viral/`. Same stem as the cut (`sh01_…`) so cut vs finish can A/B.
3. Never burn captions / type onto the cut master in place. Next pass uses `_v2` inside `viral/` if needed.
4. When `viral/approved/` is signed, move the whole job folder → [`../step-3-flywheel-organiser/`](../step-3-flywheel-organiser/).

## Skills (planned polish)

| Skill | Writes to |
|-------|-----------|
| captions (+ safe zone) | `viral/shorts/` |
| on-screen-type | `viral/shorts/` |
| cover-frame | `viral/covers/` |

Cut-engine skills stay in repo `skills/`. Influencer house skills stay in `~/.cursor/skills/`.

## Template

```bash
# New viral job = move from step-1, then ensure viral tree exists:
mkdir -p "step-2-viral-edit/{name}/viral/"{shorts,covers,approved}

# Or start from template (rare — normal path is move from step-1):
cp -r step-2-viral-edit/_template step-2-viral-edit/{name}
```
