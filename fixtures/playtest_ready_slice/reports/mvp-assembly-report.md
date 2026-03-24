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

## Missing Glue or Broken Links

- No structured playtest report exists yet.
- The temporary delivery objective glue may need to become a standalone approved system later if tuning reveals real design pressure.

## Temporary Stubs or Placeholders

- The delivery objective is implemented as assembly glue using the existing relay gate and deadline config, not as a standalone approved system module.
- The slice uses a single arena, one enemy, and one delivery target with no content variation.

## Systems Index Sync

- **Index Path**: `design/gdd/systems-index.md`
- **Systems moved to `integrated`**: Player Movement, Combat Loop
- **Status notes**: The coherent playable loop exists and is ready for a real `playtest-and-tune` pass.

## Known Blockers

- Local dev dependencies may still need installation in a fresh workspace before the scene can be launched.
- Timing, readability, and pressure have not been tuned through a documented playtest pass yet.

## Recommended Next Step

- Run `/playtest-and-tune combat-readability` after installing the project dev dependencies and launching the slice.
- Return to `/implement-system Delivery Objective` only if tuning shows that the current relay-gate glue is insufficient as an MVP objective.
