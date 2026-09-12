# Playbook Catalog

Reusable production recipes. Copy or reference via `playbook_id` in a project's `pipeline.json`.

**Flywheel strategies (peer models):** [`../flywheel-strategies.md`](../flywheel-strategies.md) · [`../flywheel-strategies-visual.md`](../flywheel-strategies-visual.md)

| ID | File | Strategy |
|----|------|----------|
| `flywheel-shorts` | [flywheel-shorts.json](flywheel-shorts.json) | Shorts queue = product; mine long source |
| `flywheel-episode` | [flywheel-episode.json](flywheel-episode.json) | Chapter = service; shorts wrap it |
| `timelapse-montage` | [timelapse-montage.json](timelapse-montage.json) | Silent visual montage (hikmat) |
| `podcast-chapter` | [podcast-chapter.json](podcast-chapter.json) | Single library chapter, no flywheel |

## Add a playbook

```bash
cp planning/playbooks/flywheel-shorts.json planning/playbooks/my-playbook.json
# Edit playbook_id, module_order, technical_modules, narrative_modules, acts
```

## Wire to a project

```json
{
  "project_id": "my-project",
  "playbook_id": "flywheel-shorts"
}
```

See [`../playbooks.md`](../playbooks.md) for architecture visuals.
