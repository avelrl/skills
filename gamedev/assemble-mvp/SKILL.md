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
- may create or update scene wiring, state flow, UI or presentation glue, restart flow, stub content, and build scripts
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
7. When the stack supports it cheaply, add or update one repeatable sanity command or checklist for the assembled loop instead of relying only on ad hoc manual checks.
8. Prefer repo-native verification commands for the chosen runtime over ambient external tooling that is not part of the repo or platform contract.
9. If specialist QA tooling is unavailable but the primary run target already proved the loop, record the exact blocker without downgrading an otherwise verified playable slice to `Blocked`.
10. For browser projects, treat browser-open, screenshot, or specialist visual probes as supporting evidence unless the repo explicitly owns that automation path.
11. Write `reports/mvp-assembly-report.md` from the canonical template and record the actual verification commands, observed loop, and real blockers.
12. Update `design/gdd/systems-index.md` when present so systems verified inside the main playable loop move to `integrated`.
13. If assembly evidence closes one or more `High-Risk Systems` rows, update their notes and the progress snapshot in the same pass instead of leaving them stale.
14. Sync matching system GDDs so their status blocks and acceptance criteria reflect the new integrated state instead of leaving them at prototype-era status.
15. Save accepted evidence in stable project paths under `reports/` or another versioned folder; do not rely only on ignored scratch dirs.
16. Update `README.md` when needed so install, run, build, test, and smoke commands match the assembled repo.
17. List missing glue, blocked systems, and obvious follow-up work without trying to solve everything in one pass. If unresolved high-risk rows remain, name the next evidence-closing move instead of implying full closure.

Failure / Stop Conditions:
- stop if the scaffold is missing or cannot boot
- stop if there are not enough implemented systems to form a loop
- stop if the request is really asking for tuning rather than assembly
- stop if the loop cannot actually be run or verified; do not write an optimistic `Playable` report
- do not treat missing optional specialist QA tooling as assembly failure when repo-native verification already proved the loop
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
- use platform specialists only for runtime-specific QA or presentation depth; keep the assembly report and integration-state sync here
- use `playtest-and-tune` after this skill to improve pacing and feel
