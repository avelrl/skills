# Gamedev Guide

Human-facing guide for using the repo's `gamedev` flow without reverse-engineering the skills first.

Related docs:

- quickstart: `docs/gamedev-quickstart.md`
- assets guide: `docs/gamedev-assets.md`
- troubleshooting: `docs/gamedev-troubleshooting.md`
- glossary: `docs/gamedev-glossary.md`
- canonical workflow: `docs/gamedev-workflow.md`
- OpenGame adaptation notes: `docs/opengame-adoption.md`

## Start With These Decisions

Before asking Codex to do anything substantial, fix four things up front:

1. the game idea or fantasy
2. the current milestone: concept, MVP, or demo
3. the working or documentation language
4. the player-facing language or languages

Keep the language split explicit:

- `Working / Documentation Language`: the language used for GDDs, reports, and project docs
- `Player-Facing Language(s)`: the language used in menus, HUD, prompts, and in-game copy

Do not rely on the agent to infer that split from the conversation tone.
State it directly in the first concept prompt.

## Main Route: Idea To MVP

Use this when you are still proving the core loop.

1. `setup-engine`
   Output: `docs/technical-preferences.md`
2. `map-systems`
   Output: `design/gdd/systems-index.md`
3. `design-system`
   Output: one system GDD such as `design/gdd/combat-loop.md`
4. `prototype` only when one risky question is still blocking confident design
5. `bootstrap-project`
   Output: runnable scaffold
6. `implement-system`
   Output: one approved system implemented in production code
7. `assemble-mvp`
   Output: `reports/mvp-assembly-report.md`
8. `playtest-and-tune`
   Output: `reports/playtest-report.md`

## If You Only Have A Concept And Want The First GDD

This is a common point of confusion.
`design-system` usually should not start from a lone concept file.

The normal route is:

1. `design/gdd/game-concept.md` exists
2. run `/setup-engine`
3. run `/map-systems`
4. only then call `/design-system [system-name]`

Reason:

- `design-system` depends on `design/gdd/systems-index.md`
- `systems-index` is created by `map-systems`
- without that map it is easy to write the wrong first GDD

Useful prompt:

```text
I only have `design/gdd/game-concept.md`.
Do not jump straight to `/design-system`.
First use `/setup-engine`, then `/map-systems`.
After that, recommend which system should get the first `/design-system`.
Working/documentation language: Russian.
Player-facing language(s): English.
```

## Extension Route: MVP To Demo

Use this when the playable loop already works and the next milestone is an audience-facing demo rather than basic MVP proof.

1. `prepare-demo`
   Output: `reports/demo-readiness.md`
2. `design-system` or `implement-system` for the highest-leverage demo blocker
3. `assemble-mvp` again to prove the refreshed slice still works coherently
4. `playtest-and-tune` again to validate the demo-quality baseline

`prepare-demo` is not UI-only.
It is the step where the repo names the demo contract for the whole slice:

- gameplay readability
- player guidance and onboarding
- HUD, menus, and prompts
- fail, restart, and exit flow
- placeholder policy
- asset and content gaps
- QA and verification expectations

When the same demo now depends on a real asset inventory, create or refresh `design/gdd/asset-registry.md` in parallel with `reports/demo-readiness.md`.

If the demo problem is actually missing gameplay, `prepare-demo` should surface that and route back into `design-system` or `implement-system`.
If the blocker is visual consistency or asset-source drift, create or refresh `design/gdd/art-bible.md` from `gamedev/templates/art-bible.md` and keep it aligned with the demo contract.

## What Each Step Produces

| Step | Main output | Move on when |
|------|-------------|--------------|
| `setup-engine` | `docs/technical-preferences.md` | stack, platform, and language policy are clear enough to map systems |
| `map-systems` | `design/gdd/systems-index.md` | MVP systems and high-risk systems are explicit |
| `design-system` | one system GDD | one system is implementation-ready |
| `prototype` | `prototypes/[slug]/REPORT.md` | one risky question is answered and the finding is folded back into docs |
| `bootstrap-project` | runnable scaffold | the repo boots and the layout is sane |
| `implement-system` | production code for one system | the system exists in code and docs are synced |
| `assemble-mvp` | `reports/mvp-assembly-report.md` | a real playable loop exists |
| `playtest-and-tune` | `reports/playtest-report.md` | you have evidence for the current baseline, not guesses |
| `prepare-demo` | `reports/demo-readiness.md` | demo-critical gaps and next handoffs are explicit |

`prepare-demo` may also create `design/gdd/asset-registry.md` when asset naming, provenance, placeholder control, or demo-critical replacements need a concrete contract.

## Good Prompt Shape

The most useful prompt pattern is:

```text
Create or update the next correct gamedev artifact for this project.
Game idea: ...
Current milestone: ...
Working/documentation language: ...
Player-facing language(s): ...
Target platform or stack constraints: ...
```

If you want one exact step, say it directly:

```text
Use `/design-system combat-loop`.
Write the combat system GDD in Russian.
Player-facing language is English.
Use the existing systems index and do not implement code.
```

## Rules That Prevent Most Confusion

- One `implement-system` pass should implement one approved system, not a whole feature cluster.
- `prototype` is disposable evidence, not production code.
- `assemble-mvp` proves the playable loop; it is not a hidden feature-factory step.
- `playtest-and-tune` is for focused tuning after a real run, not for guessing.
- `prepare-demo` is for demo-wide scope control, not a vague `make it prettier` request.
- `design/gdd/art-bible.md` and `design/gdd/asset-registry.md` solve different problems: style contract versus concrete inventory.
- If docs drift across languages, fix the language policy in the concept and technical-preferences docs first, then sync downstream docs.

## If You Are Not Sure Where To Start

- Start with `docs/gamedev-assets.md` if the current blocker is assets, animation, or visual consistency.
- Start with `docs/gamedev-quickstart.md` if you want ready-made prompt examples.
- Start with `docs/gamedev-troubleshooting.md` if you already have a repo and something feels wrong.
- Start with `docs/gamedev-glossary.md` if the terms themselves are still fuzzy.
