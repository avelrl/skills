# Courier Drift

Closure-sync fixture for a verified web MVP slice whose top-level docs no longer agree.

## Closure State

`Courier Drift` is currently treated here as `Stable MVP` for the current repo-native verification path.

- success path evidence already exists in `reports/playtest-report.md`
- fail and restart flow already exist in the playable scene
- this README claim is intentionally stale until the rest of the canonical docs are reconciled

## Current State

- the project already has a Vite + TypeScript + Canvas scaffold
- `Player Movement`, `Combat Loop`, and the current relay-gate delivery objective are integrated into one runnable MVP scene
- the slice has boot, play, win, loss, and restart flow
- `reports/mvp-assembly-report.md` and `reports/playtest-report.md` both exist, but they do not yet agree on the final closure wording
- several system docs still carry stale acceptance checklists even though the reports already claim integrated evidence

## Run

1. `npm install`
2. `npm run dev`

## Build

1. `npm run build`

## Next Handoff

Use `playtest-and-tune` next only to reconcile closure state against the accepted evidence. Do not broaden this fixture into new feature work.
