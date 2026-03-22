# Repo Guide

This repository is a small skill and template library with one explicit domain package: `gamedev/`.

## Read Order

1. Read this file for the repo map.
2. Read `docs/context-management.md` if the task will span multiple edits or documents.
3. Load only the layer you need:
   - `core/` for shared, domain-agnostic workflows
   - `gamedev/` for game-specific workflows, standards, and templates
   - `templates/` for shared document skeletons
   - `standards/` for shared conventions
   - `productivity/` for optional helper utilities

## Boundaries

- `core/` contains only workflows that still make sense if `gamedev/` disappears.
- `docs/` contains repository guidance and explanatory reference docs, not templates or standards.
- `templates/` contains reusable shared skeletons only.
- `standards/` contains compact shared conventions only.
- `gamedev/` contains game-specific skills, standards, and templates.
- `gamedev/_archive/` contains good but non-core gamedev material kept outside the active workflow path.
- `productivity/` contains optional utilities and must not be a dependency of `core/`.

## Defaults

- Prefer moving useful game-specific material into `gamedev/` over forcing it into the shared core.
- Keep a single canonical template per shared artifact type.
- Prefer short, direct workflows over ceremony-heavy routing skills.

## Notes

- `core/project-first` was retired in favor of this root entrypoint. See `docs/project-first-archived.md` for the archive note.
