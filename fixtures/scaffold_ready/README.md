# Courier Drift

Minimal project scaffold for the `Courier Drift` web game.

## Stack

- Vite 7
- TypeScript
- HTML5 Canvas

## Project Layout

- `src/` runtime code and placeholder scene
- `assets/` production asset drop zone
- `data/` lightweight manifest and starter content
- `tests/` smoke checks for scaffold data
- `design/gdd/` source design documents

## Run

```bash
npm install
npm run dev
```

Then open the local Vite URL in your browser.

## Build

```bash
npm run build
```

## Test

```bash
npm run test
npm run typecheck
```

## Current State

This scaffold intentionally stops at a bootable placeholder screen. Input capture is wired so the canvas loop can prove out browser integration, but the real `Player Movement` system is still pending.

## Next Handoff

Use `implement-system` next for `Player Movement`. The system is already marked as `designed` in `design/gdd/systems-index.md`, so the project is mature enough to move from scaffold into the first real gameplay implementation.
