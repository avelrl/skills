---
name: bootstrap-project
description: "Create the initial runnable game project scaffold from the approved technical preferences."
argument-hint: "[project-name]"
user-invocable: true
---

Purpose: Create the smallest runnable project scaffold that matches the approved technical preferences.

Use when:
- `docs/technical-preferences.md` exists and the project needs a real codebase
- the team wants a repeatable starting structure instead of hand-made bootstrapping
- design work is far enough along that implementation can start soon

Do not use for:
- choosing the engine or stack
- mapping the systems index from scratch
- implementing a specific gameplay system

Inputs / Required Context:
- required: `docs/technical-preferences.md`
- optional: `design/gdd/game-concept.md`, `design/gdd/systems-index.md`, and the first target system GDD
- optional explicit argument: project name or package name

Outputs / Owned Artifacts:
- owns the initial runnable project scaffold under the repository root
- owns the minimal folder structure for game code, data, assets, and tests
- owns starter `README.md` run and build instructions when missing or stale
- may create starter config files, package manifests, and placeholder entrypoints

Modes or Arguments:
- no argument: derive naming from the repository folder or concept title
- `[project-name]`: use an explicit normalized name for manifests and package metadata

Execution Rules:
1. Read `docs/technical-preferences.md` first and treat it as the source of truth for stack and constraints.
2. If `design/gdd/systems-index.md` or one or more system GDDs exist, read only enough to align naming, folder layout, and the first placeholder scene or module. Do not implement systems here.
3. Create the smallest runnable scaffold that matches the chosen stack; prefer fewer dependencies and fewer moving parts.
4. Create only the folders and files needed for a sane start, such as `src/`, `assets/`, `data/`, `tests/`, and run or build config.
5. Add one obvious entrypoint and one placeholder playable screen or scene so the project can boot successfully.
6. Write or update `README.md` with setup, run, build, and test commands when it is missing or stale.
7. Leave clear TODO markers where real implementation must replace placeholders.
8. End with the next handoff in the flow: `map-systems`, `design-system`, or `implement-system`, depending on design maturity.

Failure / Stop Conditions:
- stop if `docs/technical-preferences.md` is missing or too vague to determine the stack
- stop if the request is really asking for gameplay implementation instead of project scaffolding
- do not silently swap stacks, frameworks, or package managers without recording the reason

Return Format:
- scaffold root or key created paths
- starter run command
- starter build command
- files created or updated
- next recommended skill: `map-systems`, `design-system`, or `implement-system`

Example Invocation:
- `/bootstrap-project`
- `/bootstrap-project cursed-park-web`

Related Skills / Boundary:
- use `setup-engine` before this skill to lock the stack
- use `map-systems` if the system order is still unclear
- use `design-system` before `implement-system` when a system contract is missing
- use `assemble-mvp` only after multiple core systems exist in code
