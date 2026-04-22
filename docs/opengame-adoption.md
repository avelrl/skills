# OpenGame Adaptation Notes

This document records what was borrowed from the external `OpenGame` repository, what was adapted into this repo, and what was intentionally left out.

Source repository:

- GitHub: `https://github.com/leigest519/OpenGame`
- Local inspection clone used during research: `/tmp/OpenGame`

## Why This Exists

The goal was not to copy `OpenGame` wholesale.
The goal was to extract ideas that improve this repo's skill library while preserving the repo boundaries defined in `AGENTS.md` and `docs/gamedev-specialist-handoffs.md`.

The key boundary was:

- keep `gamedev/` platform-agnostic and artifact-oriented
- keep browser- or Phaser-specific depth out of the main contour unless it can be stated generically
- allow browser-specific ideas to live as optional overlays under `experimental/`

## Main Source Areas Reviewed

The most useful source areas in `OpenGame` were:

- `agent-test/docs/README.md`
- `agent-test/docs/gdd/core.md`
- `agent-test/docs/asset_protocol.md`
- `agent-test/docs/debug_protocol.md`
- `agent-test/docs/modules/*/design_rules.md`
- `agent-test/docs/modules/*/template_api.md`
- `agent-test/template-skill/README.md`
- `agent-test/debug-skill/README.md`
- `agent-test/test-cases/game-test.ts`

## What We Added To The Main Contour

### 1. Asset Registry Template

Added:

- `gamedev/templates/asset-registry.md`

Related doc updates:

- `docs/gamedev-assets.md`
- `docs/gamedev-guide.md`
- `gamedev/templates/demo-readiness.md`
- `gamedev/prepare-demo/SKILL.md`
- `gamedev/asset-audit/SKILL.md`
- `gamedev/implement-system/SKILL.md`

OpenGame influence:

- `agent-test/docs/asset_protocol.md`
- the runtime-facing asset key discipline present across their generated game flow
- the strong link between demo credibility and explicit asset expectations in their generated projects

Adaptation made here:

- we did **not** import their Phaser-specific asset-pack or animation schema
- we turned the idea into a platform-agnostic project artifact: `design/gdd/asset-registry.md`
- we made it useful for any runtime where asset paths, runtime keys, placeholder policy, or provenance can drift

Why this was worth importing:

- our repo already had `art-bible.md` for visual direction
- we were missing a concrete asset inventory and integration contract
- this closes the gap between style guidance and runtime asset usage

### 2. Stronger Demo Asset Handling

Updated:

- `gamedev/prepare-demo/SKILL.md`
- `gamedev/templates/demo-readiness.md`
- `docs/gamedev-guide.md`
- `docs/gamedev-assets.md`

OpenGame influence:

- their asset-generation contract and the way asset expectations are pushed downstream into implementation and verification

Adaptation made here:

- we kept demo prep in our existing `prepare-demo` step
- we added the option to create `design/gdd/asset-registry.md` only when asset drift becomes a real demo risk
- we did **not** collapse demo prep into a browser-only asset pipeline

### 3. Stronger `implement-system` Discipline

Updated:

- `gamedev/implement-system/SKILL.md`

OpenGame influence:

- the file-level implementation roadmap structure in `agent-test/docs/gdd/core.md`
- their strong bias toward explicit file operations before coding

Adaptation made here:

- we did **not** adopt their engine-specific GDD structure
- we imported only the useful discipline: before editing code, write a brief file-level implementation plan
- we also linked implementation to `design/gdd/asset-registry.md` when asset references matter

Why this was worth importing:

- it reduces vague implementation passes
- it makes multi-file work more inspectable
- it fits our one-system-at-a-time `implement-system` contract

### 4. Stronger Asset Audit Expectations

Updated:

- `gamedev/asset-audit/SKILL.md`

OpenGame influence:

- consistency-first checks from `agent-test/docs/debug_protocol.md`
- their habit of checking key drift before assuming deeper runtime bugs

Adaptation made here:

- we did **not** import their Phaser-specific validation rules
- we did import the idea of checking asset registry drift, missing registered assets, and untracked high-impact assets

## What We Added To Experimental

Added:

- `experimental/README.md`
- `experimental/browser-gamedev/README.md`
- `experimental/browser-gamedev/archetypes.md`
- `experimental/browser-gamedev/browser-debug-checklist.md`
- `experimental/browser-gamedev/eval-prompt-pack.md`

### 1. Browser Archetype Overlay

OpenGame influence:

- the module taxonomy in `agent-test/docs/modules/`
- their `platformer`, `top_down`, `grid_logic`, `tower_defense`, and `ui_heavy` decomposition

Adaptation made here:

- we kept it as an optional browser overlay, not as canonical `gamedev/` doctrine
- we rewrote the archetypes in platform/problem terms rather than Phaser template terms
- we kept the handoff target inside our normal flow: `setup-engine -> map-systems -> design-system`

### 2. Browser Debug Checklist

OpenGame influence:

- `agent-test/docs/debug_protocol.md`
- their emphasis on preflight consistency checks before runtime guessing

Adaptation made here:

- we did **not** import their full evolving debug-skill pipeline
- we distilled the useful operator-facing checklist for local browser game QA
- we kept it separate from generic `gamedev/` so browser assumptions do not leak into non-browser projects

### 3. Eval Prompt Pack

OpenGame influence:

- `agent-test/test-cases/game-test.ts`
- their use of curated prompts to exercise archetypes

Adaptation made here:

- prompts were rewritten to be neutral and IP-safe
- these are seeds for future evals, not benchmark claims
- they stay in `experimental/` until proven useful in repeated runs

## What We Intentionally Did Not Import

### 1. Phaser-Specific GDD Contracts

Not imported from:

- `agent-test/docs/gdd/core.md`
- `agent-test/docs/modules/*/template_api.md`

Reason:

- too tightly bound to `main.ts`, `LevelManager.ts`, `gameConfig.json`, `asset-pack.json`, and Phaser scene structure
- that would violate our platform-agnostic `gamedev/` boundary

### 2. Template Skill Evolution Pipeline

Not imported from:

- `agent-test/template-skill/README.md`

Reason:

- interesting research direction, but too heavy for the current repo
- our repo is a skill library, not a code-template evolution runtime

### 3. Debug Skill Evolution Pipeline

Not imported from:

- `agent-test/debug-skill/README.md`

Reason:

- the cumulative protocol idea is strong, but the full reactive/proactive evolving pipeline is too large for the current repo scope
- we extracted checklist value instead of the whole machinery

### 4. Engine-Specific Template APIs

Not imported from:

- `agent-test/docs/modules/*/template_api.md`

Reason:

- these are useful only inside a concrete Phaser-template runtime
- importing them directly would make our generic workflow read like a hidden Phaser guide

## Net Result

The import from `OpenGame` was intentionally selective.

What improved:

- stronger asset contract handling
- stronger implementation planning discipline
- better browser-game experimental overlays
- explicit provenance for future maintainers

What stayed protected:

- platform-agnostic `gamedev/`
- specialist overlay boundaries
- the separation between canonical workflow docs and experimental browser notes
