---
name: playtest-and-tune
description: "Run a focused playtest pass on the current build and tune the MVP without broadening scope."
argument-hint: "[focus-area]"
user-invocable: true
---

Purpose: Evaluate the current playable build, fix obvious friction, and tune the smallest set of values needed for a better MVP loop.

Use when:
- a playable slice already exists
- timing, readability, feel, or pacing problems are visible in the current build
- the team wants one focused tuning pass with a written outcome

Do not use for:
- first-time integration of systems
- large feature additions disguised as tuning
- speculative balancing before the game loop can actually be played

Inputs / Required Context:
- required: a runnable coherent playable loop that has already been assembled
- optional: `reports/mvp-assembly-report.md`, `design/gdd/systems-index.md`, relevant design docs, and previous prototype reports
- optional explicit argument: focus area such as combat, pacing, pickups, readability, or controls

Outputs / Owned Artifacts:
- owns one focused tuning pass on the current build only after a real pre-change run
- owns `reports/playtest-report.md` only when a real tuning pass actually happened
- may update constants, spawn values, timing, UI feedback, collision or recovery windows, and small QoL logic
- uses `gamedev/templates/playtest-report.md`

Modes or Arguments:
- no argument: run a general MVP sanity pass
- `[focus-area]`: bias the session toward one concern such as `combat-readability` or `pickup-pressure`

Execution Rules:
1. Before changing anything, verify that a coherent playable loop exists and can actually be run in the current environment.
2. If the loop is missing or the build does not start, stop immediately and route back to `assemble-mvp` or `implement-system`; do not write `reports/playtest-report.md` and do not make tuning edits.
3. Run the current build and observe one focused playtest pass before changing values.
4. Identify the smallest set of changes that would most improve readability, feel, pacing, or control clarity.
5. Tune values and lightweight feedback only; do not expand content scope during tuning.
6. Re-run the build after changes and compare the result to the original state.
7. Write `reports/playtest-report.md` using the canonical template and record what changed and why.
8. If a tuning change becomes the new accepted default, sync the relevant GDD or record an explicit follow-up path; do not silently contradict design docs.
9. Recommend either another small tuning pass or the next production step.

Failure / Stop Conditions:
- stop if no coherent playable loop exists yet; route back to `assemble-mvp` or `implement-system`
- stop if the build does not run at all; route back to `assemble-mvp` or `implement-system`
- do not emit `reports/playtest-report.md` for a blocked run
- stop if the request is really a major redesign instead of a tuning pass
- do not hide major structural problems behind endless constant tweaking

Return Format:
- focus area
- changes made
- observed improvement or lack of improvement
- report path
- docs synced or follow-up path recorded
- next recommended skill: `implement-system`, `assemble-mvp`, or another `playtest-and-tune`

Example Invocation:
- `/playtest-and-tune`
- `/playtest-and-tune combat-readability`

Related Skills / Boundary:
- use `assemble-mvp` before this skill so there is a coherent playable loop and a real run target
- use `implement-system` if a missing mechanic, not tuning, is the real blocker
