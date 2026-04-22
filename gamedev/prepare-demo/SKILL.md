---
name: prepare-demo
description: "Define the first audience-facing demo contract from a proven playable MVP and route the follow-up UI, asset, and presentation work."
argument-hint: "[demo-name]"
user-invocable: true
---

Purpose: Turn a working MVP slice into a concrete demo plan across gameplay, onboarding, UI, asset, and QA layers without immediately collapsing into ad hoc polish work.

Use when:
- a coherent playable loop already exists and the next milestone is an audience-facing demo, pitch build, or polished slice
- the team needs to decide which gameplay, presentation, onboarding, menu, HUD, asset, and QA gaps are actually demo-critical
- runtime-specific specialists need a clear contract before deeper UI or asset work starts

Do not use for:
- first-time MVP assembly
- a focused tuning pass on an already-defined demo target
- direct implementation of one UI or presentation system without first deciding the demo scope

Inputs / Required Context:
- required: a runnable playable loop or durable evidence that one already exists
- optional: `reports/mvp-assembly-report.md`, `reports/playtest-report.md`, `design/gdd/systems-index.md`, `docs/technical-preferences.md`, and relevant system GDDs
- optional explicit argument: demo name or milestone label

Outputs / Owned Artifacts:
- owns `reports/demo-readiness.md`
- may update `design/gdd/systems-index.md` when demo-critical presentation or meta systems need to be added, clarified, or reprioritized
- may create or update `design/gdd/asset-registry.md` when placeholder policy, asset naming, provenance, or replacement tracking needs a concrete project artifact
- may update `docs/technical-preferences.md` when specialist guidance sources for UI, assets, or QA are still missing
- uses `gamedev/templates/demo-readiness.md`

Modes or Arguments:
- no argument: prepare the smallest credible next demo from the current playable baseline
- `[demo-name]`: label the demo target explicitly

Execution Rules:
1. Verify that a coherent playable loop exists already. If the slice cannot actually be run and there is no durable proof of the loop, stop and route back to `assemble-mvp`.
2. Read `reports/mvp-assembly-report.md` or equivalent durable evidence first when it exists. Treat the current playable baseline as the starting point instead of reimagining the game from scratch.
3. Define what this demo must prove to a player, tester, stakeholder, or publisher in the first few minutes.
4. Separate demo-critical gaps from nice-to-have polish. Focus on gameplay readability, player guidance, onboarding, HUD, menus, fail and restart flow, asset readiness, performance confidence, and presentation consistency.
5. Inventory the systems that the demo now depends on. Add or refresh rows in `design/gdd/systems-index.md` when the current docs understate real demo-critical presentation or meta systems.
6. Prefer turning broad demo wishes into a small set of named systems such as `player-guidance`, `combat-readability`, `hud`, `main-menu`, `pause-and-restart`, `interaction-feedback`, or `tutorial-prompts` instead of leaving them as vague polish notes.
7. Record which runtime-specific specialist guidance should shape the next implementation pass for UI, asset pipeline, or QA. Do not duplicate that doctrine inside this skill.
8. Keep placeholder policy explicit. Name which placeholders are acceptable for the demo and which ones must be replaced before the demo is considered credible.
9. If asset naming, source provenance, runtime-key drift, or replacement tracking is becoming a real demo risk, create or refresh `design/gdd/asset-registry.md` from the canonical template instead of leaving those details scattered across notes.
10. Write `reports/demo-readiness.md` from the canonical template and include a recommended execution order for the next workflow steps.
11. End with the next recommended skill:
   - `design-system` if one or more demo-critical systems still need canonical GDDs
   - `implement-system` if the required systems are already designed and the work is ready for code
   - `assemble-mvp` if the current implementation changed enough that the playable slice needs fresh integration proof
   - `playtest-and-tune` if the demo contract already exists and the next move is a focused validation pass

Failure / Stop Conditions:
- stop if no coherent playable loop exists yet; route to `assemble-mvp` or `implement-system`
- stop if the request is really a direct UI build task for one known system; route to `design-system` or `implement-system` instead
- stop if the request is really a tuning-only pass on an already-defined demo contract; route to `playtest-and-tune`
- do not let demo preparation become an open-ended asset production marathon
- do not silently expand the gameplay scope just because presentation gaps were found
- do not let this step collapse into a UI-only interpretation when the demo problem is actually broader gameplay or guidance clarity

Return Format:
- demo target name or default label
- current baseline used
- demo-critical systems added or refreshed
- whether `design/gdd/asset-registry.md` was created or refreshed
- specialist overlays or guidance sources needed next
- placeholder policy or major blockers
- report path
- next recommended skill: `design-system`, `implement-system`, `assemble-mvp`, or `playtest-and-tune`

Example Invocation:
- `/prepare-demo`
- `/prepare-demo first-public-demo`

Related Skills / Boundary:
- use `assemble-mvp` before this skill so there is a real playable baseline to package
- use `design-system` after this skill when demo-critical presentation systems still need canonical specs
- use `implement-system` after this skill for one approved presentation or support system at a time
- use platform specialists for runtime-specific UI, asset, and QA depth; keep the demo contract and status sync here
- use `playtest-and-tune` after the demo-critical work lands and the refreshed slice can be exercised
