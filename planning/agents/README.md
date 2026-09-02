# Agent Roster

Specialized roles for the content pipeline. Each agent is a **task boundary** — train instincts and skills per role before combining into automations.

## Pipeline Flow

```
ORCHESTRATOR
    ├── TRANSCRIBER
    ├── CHAPTER PLANNER ──┐
    ├── SHORTS PLANNER  ──┼──► manifest.json
    ├── QA REVIEWER (optional gate)
    └── RENDERER
```

## Agents

| Agent | Doc | Phase | Primary output |
|-------|-----|-------|----------------|
| Orchestrator | [orchestrator.md](orchestrator.md) | 5 | Run coordination, routing |
| Transcriber | [transcriber.md](transcriber.md) | 2 | Full transcript JSON |
| Chapter Planner | [chapter-planner.md](chapter-planner.md) | 2 | `chapters[]` in manifest |
| Shorts Planner | [shorts-planner.md](shorts-planner.md) | 2 | `shorts[]` in manifest |
| Renderer | [renderer.md](renderer.md) | 3 | MP4 files |
| QA Reviewer | [qa-reviewer.md](qa-reviewer.md) | 5 | Pass/fail + fix list |

## Shared Requirements

Every agent MUST read before acting:

1. [instincts/content-pipeline.md](../instincts/content-pipeline.md)
2. Relevant platform skill from `skills/` (if applicable)
3. JSON schemas from `planning/schemas/` (if producing/consuming structured data)

## Training an Agent Around a Role

To spin up a dedicated Cursor agent for a role:

1. Copy the role doc into the agent's system context or skill bundle
2. Attach only the skills listed in that role's **Skills** section
3. Attach instincts from `planning/instincts/`
4. Restrict tool access to what the role needs (e.g. Renderer gets shell+ffmpeg, Planner gets read transcript + write manifest)
5. Test with a single artifact (one chapter plan, one render batch) before full orchestration

## Handoff Protocol

| From | To | Artifact |
|------|-----|----------|
| Orchestrator | Transcriber | input file path |
| Transcriber | Chapter Planner | `subtitles/{stem}.json` |
| Chapter Planner | Shorts Planner | draft manifest with chapters |
| Shorts Planner | Human or QA | complete manifest |
| Human/QA | Renderer | approved manifest |
| Renderer | Orchestrator | output tree + publish_queue.csv |
