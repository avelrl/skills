# Courier Drift

Pre-assembly fixture for the first playable MVP.

## Current State

- the project already has a runnable Vite + TypeScript + Canvas scaffold
- `Player Movement` is implemented as an isolated production module
- `Combat Loop` is implemented as an isolated production module
- the playable loop is not assembled yet

## What Is Missing

- title/start flow for the slice
- scene glue that wires movement, combat, and objective pressure together
- HUD, win/loss flow, and restart loop
- `reports/mvp-assembly-report.md`

## Run

1. `npm install`
2. `npm run dev`

## Build

1. `npm run build`

## Next Handoff

Use `assemble-mvp` next. Do not rewrite `Player Movement` or `Combat Loop` from scratch; use them as the starting point for the first playable slice.
