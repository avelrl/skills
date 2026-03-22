---
name: map-systems
description: "Decompose a game concept into systems, map dependencies, and maintain the systems index."
argument-hint: "[next]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion
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
- optional: `design/gdd/game-pillars.md`, existing `design/gdd/systems-index.md`, existing system docs in `design/gdd/*.md`

Outputs / Owned Artifacts:
- owns `design/gdd/systems-index.md`
- creates `design/gdd/` if it does not exist
- uses `gamedev/templates/systems-index.md`

Modes or Arguments:
- no argument: create or refresh `design/gdd/systems-index.md`
- `next`: recommend the highest-priority next `design-system` target

Execution Rules:
1. Stop immediately if `design/gdd/game-concept.md` does not exist.
2. Enumerate explicit systems, required inferred systems, and clearly out-of-scope ideas.
3. Build dependency order across foundation, core, feature, presentation, and meta layers.
4. Assign priority tiers with a bias toward MVP and vertical-slice usefulness.
5. Create or update `design/gdd/systems-index.md` using the canonical template.
6. In `next` mode, refresh the index first if it is missing or stale, then recommend the next system to design.

Failure / Stop Conditions:
- stop if the concept is too vague to separate MVP systems from wish-list ideas
- do not write system GDDs or silently invent missing concept intent

Return Format:
- systems index path
- top MVP systems
- high-risk systems
- next recommended `design-system` target with dependency rationale

Example Invocation:
- `/map-systems next`

Related Skills / Boundary:
- hand off to `design-system` for one system at a time
- hand off to `prototype` when a high-risk system needs validation before deeper design
