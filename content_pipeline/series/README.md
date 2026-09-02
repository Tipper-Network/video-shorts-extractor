# Series State

One JSON file per content series: `{series_id}.json`

Schema: [planning/schemas/series.schema.json](../planning/schemas/series.schema.json)

Example: [planning/templates/series.example.json](../planning/templates/series.example.json)

**Project requirements** (story, cuts, outputs) live in [`projects/{series_id}/requirements.md`](../projects/README.md) — not in series JSON.

Series JSON tracks flywheel continuity and publish history only.
