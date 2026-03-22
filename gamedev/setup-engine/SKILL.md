---
name: setup-engine
description: "Choose a game engine and create a project technical-preferences document from the canonical gamedev template."
argument-hint: "[engine] [version]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, WebSearch, WebFetch
---

Purpose: Choose a game engine and create the canonical project technical-preferences document.

Use when:
- a game project needs an engine decision or a technical-preferences baseline
- the team needs one place for engine, language, budgets, and tooling defaults

Do not use for:
- system decomposition
- writing individual system GDDs
- deep architecture ADR work

Inputs / Required Context:
- optional: `design/gdd/game-concept.md`
- required in guided mode: answers about 2D or 3D, target platforms, team experience, preferred language, licensing constraints
- optional explicit arguments: engine name and version

Outputs / Owned Artifacts:
- owns `docs/technical-preferences.md`
- creates `docs/` if it does not exist
- uses `gamedev/templates/technical-preferences.md`
- marks decisions as provisional when concept or platform context is incomplete

Modes or Arguments:
- guided: `/setup-engine`
- engine only: `/setup-engine unity`
- full spec: `/setup-engine godot 4.6`

Execution Rules:
1. Read `design/gdd/game-concept.md` when it exists and extract project constraints.
2. In guided mode, ask only the minimum questions needed to narrow the engine choice.
3. If the version is missing, verify the latest stable release before using it; if it cannot be verified, mark it unresolved instead of guessing.
4. Write or update `docs/technical-preferences.md` with engine, language, conventions, performance budgets, testing defaults, and approved addons.
5. End with the next handoff in the flow: `map-systems`, then `design-system`, then `prototype`.

Failure / Stop Conditions:
- stop if guided answers are too thin to narrow the engine choice and return a short comparison instead of forcing a decision
- do not invent platform, budget, or addon decisions that the project has not made

Return Format:
- chosen or shortlisted engine
- provisional or confirmed status
- output path
- critical open decisions
- next recommended skill: `map-systems`

Example Invocation:
- `/setup-engine godot 4.6`

Related Skills / Boundary:
- use `map-systems` after engine setup to define the MVP design surface
- use `architecture-decision` later for durable technical choices beyond engine selection
