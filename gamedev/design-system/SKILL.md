---
name: design-system
description: "Write or update a game-system GDD using the canonical gamedev template."
argument-hint: "<system-name>"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion
---

Purpose: Write or update one game-system GDD from the approved systems map.

Use when:
- a system already exists in `design/gdd/systems-index.md`
- the project needs one implementable GDD for that specific system

Do not use for:
- creating the overall systems index
- inventing the game concept
- broad stage or project health analysis

Inputs / Required Context:
- required: `design/gdd/game-concept.md` and `design/gdd/systems-index.md`
- optional: `design/gdd/game-pillars.md`, existing `design/gdd/[system-name].md`, upstream or downstream system docs

Outputs / Owned Artifacts:
- owns `design/gdd/[system-name].md`
- updates the matching row in `design/gdd/systems-index.md`
- uses `gamedev/templates/game-design-document.md`

Modes or Arguments:
- `<system-name>`: normalized to kebab-case for the target GDD path

Execution Rules:
1. Parse the system name and validate that the concept and systems index exist.
2. Stop and route to `map-systems` if `design/gdd/systems-index.md` is missing.
3. Stop and refresh the systems index if the requested system is not present there.
4. Summarize the system's layer, priority, dependencies, interfaces, formulas, and assumptions.
5. Create or update `design/gdd/[system-name].md` using the canonical GDD template.
6. Update the matching row in `design/gdd/systems-index.md` so status reflects reality.

Failure / Stop Conditions:
- stop if the game concept is missing
- stop if the requested system is outside the current systems index
- record unknowns as assumptions or open questions instead of inventing detail

Return Format:
- GDD path
- systems-index status update
- key rules or decisions captured
- open questions that still block implementation
- next recommended skill: `design-system` for the next dependency or `prototype` for risk reduction

Example Invocation:
- `/design-system combat-loop`

Related Skills / Boundary:
- use `map-systems` to define the system list before writing GDDs
- use `prototype` when one mechanic is still too risky to spec confidently
