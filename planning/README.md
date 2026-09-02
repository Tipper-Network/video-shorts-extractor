# Planning Hub

Shared workspace for turning content-pipeline ideas into executable structure.

**Use this folder when:**
- Designing or changing pipeline behavior before touching code
- Defining or updating agent roles, instincts, or skills
- Reviewing what to build next (`roadmap.md`)
- Drafting manifests or series state before a run

## Relationship to THP

| Layer | Repo | Owns |
|-------|------|------|
| **Strategy** | THP `the-hard-port-os/` | What to say — series scripts, observation bank, brand voice, flywheel intent |
| **Execution** | This workspace | How to cut — transcription, manifests, platform rules, ffmpeg renders |

Cross-reference THP media docs (`THP-MEDIA-001`, `THP-MEDIA-003`) for storyline and editorial tone. Implement the tooling here.

## Layout

| Path | Purpose |
|------|---------|
| [vision.md](vision.md) | North star: goals, flywheel, success criteria |
| [pipeline-architecture.md](pipeline-architecture.md) | Technical design: plan → review → render |
| [roadmap.md](roadmap.md) | Phased build order and current status |
| [capability-matrix.md](capability-matrix.md) | Platform scripts/skills — test status per project |
| [agents/](agents/) | One doc per specialized agent role |
| [instincts/](instincts/) | Behavioral rules agents must internalize |
| [skills/](skills/) | Skill backlog, status, and mapping to agents |
| [schemas/](schemas/) | JSON contracts between pipeline stages |
| [templates/](templates/) | Copy-paste examples for manifests and queues |

## Workflow

```
1. Align on vision + architecture (edit markdown here)
2. Read THP series/script if content is THP-branded
3. Assign work via roadmap phases
4. Agent reads its role doc + instincts + linked skill
5. Agent produces/consumes artifacts matching schemas/
6. Human reviews manifest before render (until QA agent is trusted)
7. Update roadmap status when a phase ships
```

## Links

- Workspace overview: [`../README.md`](../README.md)
- Master orchestrator: [`../SKILL.md`](../SKILL.md)
- Platform skills: [`../skills/`](../skills/)
- Execution code: [`../content_pipeline/`](../content_pipeline/)
- Project requirements: [`../content_pipeline/projects/`](../content_pipeline/projects/)
- Environment setup: [`../instructions.md`](../instructions.md)
- THP content (external): `~/Desktop/The-Hard-Port-stuff/The Hard Port/the-hard-port-os/content/youtube/`

## Conventions

- **Status tags:** `planned` → `in-progress` → `shipped` → `deprecated`
- **Agent docs:** role, inputs, outputs, skills, instincts, handoffs, done-when
- **Schemas:** source of truth for JSON between scripts; code must conform
- **Don't duplicate platform rules** — link to `skills/youtube_chunks/` etc.
- **Don't duplicate THP strategy** — link to THP media docs
