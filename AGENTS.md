# Repo Guide

This repository is a small skill and template library with one explicit domain package: `gamedev/`.

## Read Order

1. Read this file for the repo map.
2. Read `docs/context-management.md` if the task will span multiple edits or documents.
3. Read `docs/gamedev-workflow.md` for the canonical full-run vs step-by-step routing when the task is game-related.
4. Read `docs/gamedev-specialist-handoffs.md` when the task needs runtime-, engine-, UI-, asset-, or QA-specific guidance.
5. Load only the layer you need:
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
- Keep `gamedev/` platform-agnostic; do not copy browser-runtime doctrine from specialist plugins into the generic flow.

## Gamedev Flow

- The active `gamedev/` path now has two core lanes plus one optional demo extension. Preproduction: `setup-engine -> map-systems -> design-system -> prototype`. Production bridge: `bootstrap-project -> implement-system -> assemble-mvp -> playtest-and-tune`. Demo extension: `prepare-demo -> design-system/implement-system -> assemble-mvp -> playtest-and-tune`.
- Typical small-game handoff: lock the stack, map systems, design the first MVP systems, prototype only where risk is real, then bootstrap the scaffold and move into implementation and playable-loop assembly. When the milestone changes from `prove the loop` to `show a credible demo`, run `prepare-demo` before broad UI, asset, or presentation work.
- The flow is platform-agnostic. Browser projects may overlay `Game Studio` or another browser specialist for runtime, UI, asset, and playtest depth. Non-browser projects should use engine-native specialists or official engine docs without changing the core flow ownership.
- `bootstrap-project` may happen as soon as `docs/technical-preferences.md` is stable and the repository needs a runnable codebase, but do not skip `map-systems` or `design-system` when system scope is still unclear.
- `implement-system` is for one approved system at a time and should push the systems index to `implemented` when code exists.
- `assemble-mvp` is only for wiring multiple implemented systems into one coherent playable loop and should push verified systems to `integrated`.
- `prepare-demo` is for defining the first audience-facing demo contract from a proven slice and should turn vague polish wishes into explicit presentation, asset, and QA handoffs.
- `playtest-and-tune` is for focused tuning after a playable slice exists.
- Keep prototype code isolated under `prototypes/`; do not quietly promote it into production.
- Prefer a small playable loop over broad feature coverage.

## Notes

- `core/project-first` was retired in favor of this root entrypoint. See `docs/project-first-archived.md` for the archive note.
