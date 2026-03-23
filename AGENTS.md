# Repo Guide

This repository is a small skill and template library with one explicit domain package: `gamedev/`.

## Read Order

1. Read this file for the repo map.
2. Read `docs/context-management.md` if the task will span multiple edits or documents.
3. Read `docs/gamedev-workflow.md` for the canonical full-run vs step-by-step routing when the task is game-related.
4. Load only the layer you need:
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

## Gamedev Flow

- The active `gamedev/` path now has two connected lanes. Preproduction: `setup-engine -> map-systems -> design-system -> prototype`. Production bridge: `bootstrap-project -> implement-system -> assemble-mvp -> playtest-and-tune`.
- Typical small-game handoff: lock the stack, map systems, design the first MVP systems, prototype only where risk is real, then bootstrap the scaffold and move into implementation and playable-loop assembly.
- `bootstrap-project` may happen as soon as `docs/technical-preferences.md` is stable and the repository needs a runnable codebase, but do not skip `map-systems` or `design-system` when system scope is still unclear.
- `implement-system` is for one approved system at a time and should push the systems index to `implemented` when code exists.
- `assemble-mvp` is only for wiring multiple implemented systems into one coherent playable loop and should push verified systems to `integrated`.
- `playtest-and-tune` is for focused tuning after a playable slice exists.
- Keep prototype code isolated under `prototypes/`; do not quietly promote it into production.
- Prefer a small playable loop over broad feature coverage.

## Notes

- `core/project-first` was retired in favor of this root entrypoint. See `docs/project-first-archived.md` for the archive note.
