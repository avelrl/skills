# Gamedev Glossary

Expanded glossary for newcomers.
This includes both workflow terms and basic production terms that appear across the repo.

| Term | Meaning |
|------|---------|
| `Working / Documentation Language` | The language used for concept docs, GDDs, reports, and project-facing documentation. |
| `Player-Facing Language(s)` | The language used in HUD, menus, prompts, subtitles, and game copy. |
| `Concept` | The high-level description of the game: what it is, who it is for, and what makes it worth building. |
| `Game Concept` | The concrete document `design/gdd/game-concept.md`. |
| `System` | One meaningful part of the game with clear boundaries, such as movement, combat, camera, or menu flow. |
| `Systems Index` | The project-wide map of systems and their statuses in `design/gdd/systems-index.md`. |
| `GDD` | A game design document for one system or one project-level design surface. |
| `Pillars` | A small set of core design principles used to protect the game's identity and reject weak ideas. |
| `Stack` | The main technical combination for the project: engine, language, platform, and major libraries. |
| `Runtime / Engine` | The environment the game runs in, such as Web, Unity, Unreal, or Godot. |
| `Scaffold` | The minimal runnable project structure: folders, entrypoint, build path, and basic startup flow. |
| `Artifact` | A concrete output of a workflow step, such as a document, report, index, or scaffold. |
| `Prerequisite` | A condition or artifact that must exist before the next step can be done cleanly. |
| `Handoff` | An explicit pointer to the next correct step or owner after the current one finishes. |
| `Prototype` | Disposable evidence used to answer one risky question before production implementation. |
| `High-Risk System` | A system that can seriously affect scope, schedule, architecture, or game quality if it is still unclear. |
| `MVP` | The smallest playable version that proves the core hypothesis of the game. |
| `Playable Loop` | A real boot-to-play-to-fail-or-exit path that can be executed in one run. |
| `Vertical Slice` | A narrower but more polished slice than a rough MVP. |
| `Demo` | An audience-facing build meant to communicate the game clearly, not just prove the loop exists. |
| `Demo Contract` | The explicit list of what a demo must prove, show, and support for its intended audience. |
| `Prepare-Demo` | The step that defines the demo contract, gaps, placeholders, specialist handoffs, and next build-up order. |
| `Onboarding` | The first-minutes player experience: goals, controls, hints, and basic understanding. |
| `HUD` | Persistent in-play interface elements such as health, resources, objectives, and prompts. |
| `Placeholder` | A temporary stand-in for a final asset, text, mechanic, or screen. |
| `Asset` | A visual, audio, or other production file used by the game. |
| `Asset Pipeline` | The rules and path for creating, importing, replacing, and validating assets. |
| `Playtest` | A real run of the game used to observe player-facing behavior and friction. |
| `Smoke Check` | A short sanity check that the project boots and is not broken in the most basic paths. |
| `Tuning` | Targeted adjustment of existing values, pacing, readability, or feel after a real run. |
| `Localization` | Preparing the project to support more than one language consistently. |
| `Porting` | Moving the game from one stack or platform to another. |
| `Closure` | The point where a step can honestly be considered complete based on artifacts and verification. |
| `Specialist Overlay` | Platform-specific depth layered on top of the generic `gamedev` flow, such as browser UI or asset pipeline guidance. |
