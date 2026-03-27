# Courier Drift

Closure-repeatability fixture for a web MVP slice that looks finished until the latest rerun evidence is inspected.

## Closure State

`Courier Drift` is currently described here as `Stable MVP`.

- one successful run artifact exists under `reports/evidence/`
- the integrated loop still supports boot, play, win, loss, and restart
- this closure claim is intentionally optimistic until the later failed rerun is reconciled

## Current State

- the project already has a Vite + TypeScript + Canvas scaffold
- `Player Movement`, `Combat Loop`, and the relay-gate delivery objective are integrated into one runnable MVP scene
- the slice has boot, play, win, loss, and restart flow
- the current issue is not missing gameplay; it is whether the closure claim is honest given the mixed evidence

## Run

1. `npm install`
2. `npm run dev`

## Build

1. `npm run build`

## Next Handoff

Use `playtest-and-tune` next only to reconcile repeatability evidence and the resulting closure state. Do not add features or reopen broad assembly work.
