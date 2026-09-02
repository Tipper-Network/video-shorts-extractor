# Playbook Catalog

Reusable production recipes. Copy or reference via `playbook_id` in a project's `pipeline.json`.

| ID | File | Best for |
|----|------|----------|
| `flywheel-episode` | [flywheel-episode.json](flywheel-episode.json) | THP / speech — chapters + flywheel shorts |
| `timelapse-montage` | [timelapse-montage.json](timelapse-montage.json) | Silent build logs — supercut shorts |
| `podcast-chapter` | [podcast-chapter.json](podcast-chapter.json) | Single deep-dive chapter, light social |

## Add a playbook

```bash
cp planning/playbooks/podcast-chapter.json planning/playbooks/my-new-playbook.json
# Edit playbook_id, module_order, skills[], modules
```

## Wire to a project

In `content_pipeline/projects/{name}/pipeline.json`:

```json
{
  "project_id": "my-project",
  "playbook_id": "flywheel-episode"
}
```

Or inline the full playbook (no `playbook_id`) — see hikmat.

See [`../playbooks.md`](../playbooks.md) for visuals and design guide.
