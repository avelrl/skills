# Gamedev Specialist Handoffs

Use this document to keep `gamedev/` cleanly separated from platform- or engine-specific specialist guidance.

## Core Rule

`gamedev/` is the project workflow and artifact layer for games across browser, desktop, console, mobile, and engine-native projects.

It owns:

- mode selection and prerequisite routing
- canonical project artifacts such as `docs/technical-preferences.md`, `design/gdd/systems-index.md`, system GDDs, optional shared visual contracts such as `design/gdd/art-bible.md`, prototype reports, and MVP, demo, or playtest reports
- evidence closure and status sync
- step-to-step handoffs

It does not try to be the deepest runtime specialist for every engine or platform.

## What Specialists Own

Specialist guidance owns the implementation depth that is specific to one runtime or delivery surface:

- engine or renderer architecture
- runtime-specific scaffold shape
- platform-specific UI or HUD patterns
- asset pipeline details tied to that runtime
- platform-specific QA heuristics and tooling

## Browser Overlay

When browser-game specialization is needed and OpenAI `Game Studio` is available, use it as the default game-specific specialist overlay.
When the needed surface is direct inspection or interaction with a local browser target inside Codex, use `Browser Use` as the in-app browser specialist.

| Need | Specialist Source | `gamedev/` Step Still Owns |
|------|-------------------|----------------------------|
| Browser stack choice and runtime architecture | `game-studio`, `web-game-foundations`, `phaser-2d-game`, `three-webgl-game`, `react-three-fiber-game` | `setup-engine` |
| Browser scaffold conventions | runtime specialist from `Game Studio` | `bootstrap-project` |
| Browser UI, HUD, menus, overlay direction | `game-ui-frontend` | `prepare-demo`, `bootstrap-project`, `assemble-mvp`, `playtest-and-tune` |
| 2D sprite generation workflow | `sprite-pipeline` | `prototype`, `prepare-demo`, `implement-system` |
| 3D web asset shipping | `web-3d-asset-pipeline` | `prepare-demo`, `bootstrap-project`, `implement-system` |
| Browser QA and visual review | `Browser Use` for in-app local inspection, `game-playtest` for game-specific playtest guidance, plus repo-owned smoke tooling where appropriate | `prepare-demo`, `assemble-mvp`, `playtest-and-tune` |

The specialist may supply runtime-specific implementation guidance or evidence, but the canonical reports and status updates still belong to the `gamedev/` flow.

Use `Browser Use` for quick local browser checks such as opening `localhost`, clicking through the playable loop, taking screenshots, and reading visible console signals.
Prefer repo-owned smoke or E2E commands when the project needs repeatable closure evidence.
If Browser Use evidence matters for a report, save durable screenshots or notes under a stable project path, or record a reproducible verification checklist in the canonical report.

Optional browser-specific working notes may live under `experimental/browser-gamedev/` in this repo.
Treat them as overlays or scratchpads for browser work, not as replacements for the canonical `gamedev/` artifacts or ownership rules above.

## Non-Browser Projects

For Godot, Unity, Unreal, custom engines, or proprietary runtimes:

- use official engine documentation or project-local specialists for engine-specific implementation details
- keep the same `gamedev/` flow for stack capture, systems mapping, GDDs, prototypes, implementation scope, MVP assembly, demo preparation, and tuning reports
- record engine-specific constraints in `docs/technical-preferences.md` instead of cloning engine doctrine into generic skill text

## Anti-Duplication Rules

- Do not encode Phaser, Three.js, React Three Fiber, or browser-UI defaults directly into generic `gamedev/*/SKILL.md` unless the rule is truly platform-agnostic.
- Do not bake Browser Use, Playwright, or browser-only QA expectations into generic MVP assembly or tuning logic.
- Do not make templates require browser-only artifacts.
- Do not let cheap web fixtures redefine the whole repo as browser-only.
- Do not treat Browser Use availability as a generic completion gate; missing in-app browser tooling is not a blocker when repo-native verification already proved the loop.

## Step Ownership Reference

- `setup-engine`: capture the chosen stack and record which specialist source informed the decision when the project needs one.
- `map-systems`: stay platform-agnostic and focus on gameplay decomposition, dependencies, and risk.
- `design-system`: keep system contracts generic unless a platform or engine constraint is genuinely part of the design.
- `prototype`: answer one risky question with disposable evidence, regardless of platform.
- `bootstrap-project`: own the scaffold contract and repo hygiene; let specialists shape runtime-specific folder and architecture defaults.
- `implement-system`: own one-system-at-a-time scope and doc sync; use specialists for runtime-specific implementation patterns when needed.
- `assemble-mvp`: own playable-loop closure, durable evidence, and integration status.
- `prepare-demo`: own the demo contract, the inventory of demo-critical presentation systems, the placeholder policy, the specialist handoff capture, and the decision of whether the project now needs a refreshed `design/gdd/art-bible.md`.
- `playtest-and-tune`: own the accepted tuning changes, report, and canonical doc sync even when specialist QA tools are used.
