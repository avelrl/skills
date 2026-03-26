---
name: assemble-mvp
description: "Integrate implemented systems into one small playable MVP or vertical slice."
argument-hint: "[slice-name]"
user-invocable: true
---

Purpose: Stitch already implemented systems into one coherent playable loop.

Use when:
- the project already has a runnable scaffold plus multiple implemented systems
- the team wants a vertical slice or MVP build instead of isolated subsystems
- integration glue, scene wiring, flow control, and fail states are the main work left

Do not use for:
- first-time project scaffolding
- implementing a single isolated system from scratch
- broad tuning passes before the loop even works end to end

Inputs / Required Context:
- required: runnable project scaffold
- required: at least two implemented systems in main project code
- optional: `design/gdd/game-concept.md`, `design/gdd/systems-index.md`, and `docs/technical-preferences.md`
- optional explicit argument: slice or milestone name

Outputs / Owned Artifacts:
- owns the integration work needed for one playable MVP or vertical slice
- owns `reports/mvp-assembly-report.md`
- may create or update scene wiring, state flow, HUD glue, restart flow, stub content, and build scripts
- may create or update one lightweight repeatable smoke or sanity entrypoint when the stack supports it cheaply
- uses `gamedev/templates/mvp-assembly-report.md`

Modes or Arguments:
- no argument: assemble the smallest current MVP loop
- `[slice-name]`: label the assembly report and target a named slice

Execution Rules:
1. Inventory implemented systems and identify the minimum playable loop available right now.
2. Read `design/gdd/systems-index.md` when it exists so integration status and unresolved `High-Risk Systems` rows can be updated accurately.
3. Integrate only what is needed for one coherent slice: boot, play, feedback, fail, and restart or exit.
4. Prefer glue code, placeholders, and one arena or scene over expanding content breadth.
5. Ensure controls, core interaction, objective pressure, fail state, and restart or exit flow are actually reachable in one run.
6. Run the actual build or game target before writing the report; do not backfill `reports/mvp-assembly-report.md` from assumptions.
7. When the stack supports it cheaply, add or update one repeatable smoke or sanity command for the assembled loop instead of relying only on ad hoc manual clicking.
8. Prefer repo-native verification commands over ambient browser CLI probes that depend on a separately installed Playwright browser stack.
9. If a secondary browser probe fails only because the environment lacks an installed browser or similar tool-layer prerequisite, record the exact blocker but do not downgrade an otherwise verified playable loop to `Blocked`.
10. Write `reports/mvp-assembly-report.md` from the canonical template and record the actual verification commands, observed loop, and real blockers.
11. Update `design/gdd/systems-index.md` when present so systems verified inside the main playable loop move to `integrated`.
12. If assembly evidence closes one or more `High-Risk Systems` rows, update their notes and the progress snapshot in the same pass instead of leaving them stale.
13. Sync matching system GDDs so their status blocks and acceptance criteria reflect the new integrated state instead of leaving them at prototype-era status.
14. Save accepted evidence in stable project paths under `reports/` or another versioned folder; do not rely only on ignored scratch dirs.
15. Update `README.md` when needed so install, run, build, test, and smoke commands match the assembled repo.
16. List missing glue, blocked systems, and obvious follow-up work without trying to solve everything in one pass. If unresolved high-risk rows remain, name the next evidence-closing move instead of implying full closure.

Failure / Stop Conditions:
- stop if the scaffold is missing or cannot boot
- stop if there are not enough implemented systems to form a loop
- stop if the request is really asking for tuning rather than assembly
- stop if the loop cannot actually be run or verified; do not write an optimistic `Playable` report
- do not treat a missing optional Playwright browser install as assembly failure when repo-native verification already proved the loop
- do not turn this skill into an all-systems implementation marathon

Return Format:
- assembled slice name or default MVP label
- playable loop now supported
- files created or updated
- report path
- systems moved to `integrated`, if any
- high-risk rows closed or still unresolved, if any
- blockers or next gaps
- next recommended skill: `playtest-and-tune`

Example Invocation:
- `/assemble-mvp`
- `/assemble-mvp first-playable`

Related Skills / Boundary:
- use `implement-system` before this skill to build the ingredients
- use `playtest-and-tune` after this skill to improve pacing and feel
