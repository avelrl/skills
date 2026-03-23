---
name: map-systems
description: "Decompose a game concept into systems, map dependencies, and maintain the systems index."
argument-hint: "[next]"
user-invocable: true
---

Purpose: Turn a game concept into a systems index and a clear design order.

Use when:
- `design/gdd/game-concept.md` exists and the project needs a system map
- you need the next `design-system` target from the current MVP surface

Do not use for:
- inventing the game concept itself
- writing individual system GDDs
- broad production-stage readiness assessment

Inputs / Required Context:
- required: `design/gdd/game-concept.md`
- optional: `design/gdd/game-pillars.md`, existing `design/gdd/systems-index.md`, existing system docs in `design/gdd/*.md`, relevant prototype reports in `prototypes/*/REPORT.md`

Outputs / Owned Artifacts:
- owns `design/gdd/systems-index.md`
- creates `design/gdd/` if it does not exist
- uses `gamedev/templates/systems-index.md`
- maintains a `High-Risk Systems` section inside `design/gdd/systems-index.md`

Modes or Arguments:
- no argument: create or refresh `design/gdd/systems-index.md`
- `next`: recommend the highest-priority next `design-system` target

Execution Rules:
1. Stop immediately if `design/gdd/game-concept.md` does not exist.
2. Enumerate explicit systems, required inferred systems, and clearly out-of-scope ideas.
3. Build dependency order across foundation, core, feature, presentation, and meta layers.
4. Assign priority tiers with a bias toward MVP and vertical-slice usefulness.
5. Use a fixed status vocabulary for systems and keep updates forward-only: `identified`, `designed`, `prototyped`, `informed-by-prototype`, `implemented`, `integrated`.
6. Apply the status meanings consistently:
   - `identified`: the system is only mapped in the systems index
   - `designed`: the canonical GDD exists
   - `prototyped`: a relevant prototype report exists, but its findings are not fully folded into the canonical design docs
   - `informed-by-prototype`: prototype findings and baseline decisions are reflected in the GDD or index
   - `implemented`: production code exists for the system
   - `integrated`: the implementation is wired into the main playable loop or production flow
7. Never downgrade a row when refreshing the index; keep the strongest confirmed status already evidenced.
8. Always include a compact `High-Risk Systems` section in `design/gdd/systems-index.md` with up to 5 real MVP risks, and do not pad the list with weak filler. Use:
   - `System`
   - `Risk Type`
   - `Why It Is Risky`
   - `Mitigation`
   - `Prototype Candidate`
   - `Evidence Needed`
9. If prototype reports already exist, use them to update relevant system statuses and risk notes rather than treating the index as a fresh document.
10. Create or update `design/gdd/systems-index.md` using the canonical template.
11. In `next` mode, refresh the index first if it is missing or stale, then recommend the next highest-leverage move.
12. In `next` mode, prefer a target that either:
    - unlocks multiple downstream systems, or
    - reduces a high-risk uncertainty that blocks confident design.
13. In `next` mode, if the highest-leverage move is evidence gathering rather than spec writing, recommend `prototype` before `design-system`.

Failure / Stop Conditions:
- stop if the concept is too vague to separate MVP systems from wish-list ideas
- do not write system GDDs or silently invent missing concept intent

Return Format:
- systems index path
- top MVP systems
- high-risk systems
- any system statuses updated from existing evidence
- next recommended move: `design-system` or `prototype`
- rationale for that recommendation

Example Invocation:
- `/map-systems next`

Related Skills / Boundary:
- hand off to `design-system` for one system at a time
- hand off to `prototype` when a high-risk system needs validation before deeper design
