# First Playable - MVP Assembly Report

## Status

- **Report Path**: `reports/mvp-assembly-report.md`
- **Date**: 2026-03-24
- **Slice**: First Playable
- **Build or Run Target**: `npm install && npm run dev`
- **Assembly State**: Playable

## Goal

Prove one coherent run where the player starts the slice, uses the implemented movement and combat systems to defeat the interceptor, reaches the relay gate before the deadline, and can fail or restart cleanly.

## Integrated Systems

| System | Current Role In Loop | Verified In Build? | Notes |
|--------|----------------------|--------------------|-------|
| Player Movement | Traversal, dodging, melee lunge control | Ready for playtest | Wired into the first playable scene with keyboard input and restart flow. |
| Combat Loop | Enemy chase, telegraph, strike, damage exchange | Ready for playtest | Wired into the same run state as movement; enemy defeat unlocks the delivery gate. |
| Delivery Objective | Gate unlock, deadline pressure, extraction finish | Ready for playtest | The relay gate and deadline glue already produce a full win/loss loop in the current scene. |

## Playable Loop

- **Boot flow**: A title overlay introduces the slice and starts the run on `Enter`.
- **Core interaction loop**: Move with `WASD` or arrows, avoid telegraphed strikes, then attack with `Space` to defeat the interceptor.
- **Objective or pressure**: A 40-second deadline counts down; the relay gate stays locked until the enemy is defeated.
- **Fail state**: The run ends if player health reaches zero or the deadline expires.
- **Restart or exit flow**: `Enter` or `R` restarts the run from a clean state. No explicit exit flow is implemented.

## What Works Now

- One main scene owns boot, play, win, loss, and restart state instead of a placeholder assembly preview.
- Existing Player Movement and Combat Loop modules run together inside the same arena with HUD feedback and gate unlock progression.
- The relay gate, countdown timer, enemy HP, player HP, and outcome overlays provide enough feedback for a focused playtest pass.
- The current repo already carries a later tuning report, but this assembly report has not yet been reconciled to that accepted closure read.

## Missing Glue or Broken Links

- No code-side glue blocker remains for the current MVP loop.
- Canonical closure docs still disagree on whether the slice should stop at `Playable` or `Stable MVP`.
- Several matching system docs still carry stale acceptance checklists despite the current reports claiming integrated evidence.

## Temporary Stubs or Placeholders

- The delivery objective is implemented as assembly glue using the existing relay gate and deadline config, not as a standalone approved system module.
- The slice uses a single arena, one enemy, and one delivery target with no content variation.

## Systems Index Sync

- **Index Path**: `design/gdd/systems-index.md`
- **Systems moved to `integrated`**: Player Movement, Combat Loop, Delivery Objective
- **Status notes**: The coherent playable loop exists, later tuning evidence already exists, and the remaining issue is honest closure sync across canonical docs.

## Known Blockers

- Local dev dependencies may still need installation in a fresh workspace before the scene can be launched.
- No structural blocker remains for the current MVP loop, but closure wording and status sync are stale across the canonical docs.

## Recommended Next Step

- Reconcile the current closure state against `reports/playtest-report.md` and the accepted evidence before calling this slice done.
- Reopen `/playtest-and-tune` only if that reconciliation reveals a real unresolved pacing or readability blocker.
