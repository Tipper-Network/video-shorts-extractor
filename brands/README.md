# Brands — operator data

A **brand file** is what the planner reads before cutting. The video title picks the entity; this folder holds that entity’s book.

Not in git. Clone the repo, copy the template, fill yours.

```bash
cp brands/_template.md brands/my-brand.md
```

Point the project at it: set **Entity** in `projects/{name}/requirements.md` to the same name as the file stem (`my-brand`).

## Shape

See [`_template.md`](_template.md). Minimum: who it’s for, what a short may keep, what to park, words you never put on a public cut.

This workspace’s local operator pack (Tipper / THP / GAF) lives here on disk and stays local. Do not treat those books as part of the product.

## Website later

Same contract: account uploads or selects a brand record; the agent loads it the way it loads `brands/{entity}.md` today.
