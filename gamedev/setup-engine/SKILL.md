---
name: setup-engine
description: "Choose a game engine or runtime direction and create a project technical-preferences document from the canonical gamedev template."
argument-hint: "[runtime-or-engine] [version-or-language]"
user-invocable: true
---

Purpose: Choose a game engine or runtime direction and create the canonical project technical-preferences document.

Use when:
- a game project needs a runtime direction or a technical-preferences baseline
- the team needs one place for engine or runtime, target platforms, language, budgets, and tooling defaults

Do not use for:
- system decomposition
- writing individual system GDDs
- deep architecture ADR work

Inputs / Required Context:
- optional: `design/gdd/game-concept.md`
- required in guided mode: answers about 2D or 3D, target platforms, team experience, preferred language, licensing constraints
- optional explicit arguments: engine or runtime name plus version or language

Outputs / Owned Artifacts:
- owns `docs/technical-preferences.md`
- creates `docs/` if it does not exist
- uses `gamedev/templates/technical-preferences.md`
- marks decisions as provisional when concept or platform context is incomplete

Modes or Arguments:
- guided: `/setup-engine`
- runtime only: `/setup-engine web`
- runtime spec: `/setup-engine web typescript`
- engine spec: `/setup-engine unity 6`
- engine spec: `/setup-engine unreal 5.6`

Execution Rules:
1. Read `design/gdd/game-concept.md` when it exists and extract project constraints.
2. In guided mode, ask only the minimum questions needed to narrow the engine or runtime choice.
3. If the version is missing, verify the latest stable release before using it; if it cannot be verified, mark it unresolved instead of guessing.
4. If the target runtime is browser-based, use `Game Studio` when available as the runtime-specialist source for stack-specific guidance instead of copying Phaser, Three.js, or browser-UI doctrine into this skill.
5. If the target runtime is not browser-based, rely on official engine docs or project-local specialists for engine-specific implementation details instead of inventing a parallel doctrine here.
6. Write or update `docs/technical-preferences.md` with runtime or engine, target platforms, language, conventions, performance budgets, testing defaults, and approved addons.
7. End with the next handoff in the flow: `map-systems`, then `design-system`, then `prototype`.

Failure / Stop Conditions:
- stop if guided answers are too thin to narrow the runtime choice and return a short comparison instead of forcing a decision
- do not invent platform, budget, or addon decisions that the project has not made

Return Format:
- chosen or shortlisted runtime or engine
- provisional or confirmed status
- output path
- specialist source used, if any
- critical open decisions
- next recommended skill: `map-systems`

Example Invocation:
- `/setup-engine web typescript`
- `/setup-engine unity 6`
- `/setup-engine unreal 5.6`

Related Skills / Boundary:
- use `map-systems` after engine setup to define the MVP design surface
- use browser specialists such as `Game Studio` only for browser-runtime depth; keep `docs/technical-preferences.md` as the canonical artifact here
- use `architecture-decision` later for durable technical choices beyond engine selection
