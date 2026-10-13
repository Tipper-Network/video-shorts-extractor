# Integrations

| Folder | Purpose |
|--------|---------|
| [`google-sheets/`](google-sheets/) | Publish catalog sync (schedule, titles, status) |
| [`platforms/`](platforms/) | Direct YouTube / Instagram / TikTok upload (no Postiz SaaS) |

Sheet = truth for titles + dates. Platform adapters upload the `video_path` from each approved row.
