---
paths:
  - "assets/data/**"
---

# Data File Rules

- Use a consistent machine-readable format and keep every file valid.
- Keep filenames predictable and lowercase with underscores.
- Document the schema or field contract somewhere the team can actually find.
- Separate authoring data from derived/generated data when both exist.
- Use explicit defaults for optional fields; do not rely on guesswork in loaders.
- When a schema changes incompatibly, version it or document the migration path.
- Remove or flag orphaned entries that are no longer referenced by code or content.
