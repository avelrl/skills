# Gamedev Assets Guide

Practical guidance for adding art, UI assets, audio-adjacent visual content, and animation decisions inside the repo's `gamedev` flow.

Related docs:

- human-facing guide: `docs/gamedev-guide.md`
- canonical workflow: `docs/gamedev-workflow.md`
- specialist boundaries: `docs/gamedev-specialist-handoffs.md`
- quickstart prompts: `docs/gamedev-quickstart.md`
- OpenGame adaptation notes: `docs/opengame-adoption.md`

## Core Rule

`gamedev/` owns asset timing, placeholder policy, canonical documents, and handoffs.
It does not try to be the deepest production pipeline for every runtime.

That split matters:

- use `gamedev/` to decide when placeholder art is acceptable
- use `prepare-demo` to lock what must be replaced before a real demo
- use specialists or external tools for runtime-specific asset production depth
- use `asset-audit` to check naming, formats, references, and obvious drift after assets land

## Where Assets Fit In The Flow

### Early Preproduction

During `setup-engine`, `map-systems`, and early `design-system`, capture only the visual constraints that affect gameplay or tooling:

- target look and fidelity
- platform budgets
- readability-sensitive systems such as combat telegraphs or dense HUDs
- whether the project expects pixel sprites, painted 2D, or shipped 3D assets

Do not turn this phase into mass asset production.

### MVP Work

During `prototype`, `bootstrap-project`, and early `implement-system`, placeholders are normal.
Prefer the smallest assets that let the team test interaction, clarity, scale, and pacing.

Typical placeholder-safe areas:

- temporary props
- rough backgrounds
- temp UI panels
- unpolished VFX
- test-only character art

### Demo Transition

When the milestone changes from `prove the loop` to `show a credible demo`, run `prepare-demo`.
That is where the project should explicitly record:

- which placeholders are still acceptable
- which assets must be replaced before the demo
- which asset classes now need a stable production pipeline
- which specialist guidance should shape the next asset or animation pass

If visual consistency or source drift becomes a real blocker, create or refresh `design/gdd/art-bible.md`.

When concrete asset naming, source tracking, placeholder control, or import sanity becomes messy, also create or refresh `design/gdd/asset-registry.md`.

## What The Asset Registry Is

`design/gdd/asset-registry.md` is the concrete inventory and integration contract for assets that matter to the current milestone.
Use `gamedev/templates/asset-registry.md` as the canonical template.

It is the right place to capture:

- runtime keys or paths that code and data should use
- which assets are final, placeholder, planned, or must be replaced before demo
- which scenes or systems depend on each asset group
- source provenance when the team mixes AI outputs, packs, hand-made art, or contractor work
- replacement queues when demo readiness depends on a small set of higher-quality assets

It is not:

- the project's visual identity document
- a replacement for `design/gdd/art-bible.md`
- a giant warehouse dump of every file under `assets/`
- a reason to freeze MVP work until every placeholder is cleaned up

## When To Create The Asset Registry

Create or refresh it when one of these becomes true:

- the same asset is now referenced from multiple scenes or systems
- placeholder drift is causing import, naming, or ownership confusion
- multiple asset sources are being mixed and provenance now matters
- the team needs a credible demo and must separate acceptable placeholders from must-replace assets
- `asset-audit` is finding the same naming or reference problems repeatedly

For a tiny project, keep it short.
The goal is operational clarity, not inventory bureaucracy.

## How To Use The Asset Registry

1. Start from `gamedev/templates/asset-registry.md`.
2. Save the project copy as `design/gdd/asset-registry.md` unless the project already has a stronger asset-tracking structure.
3. Track only the assets that affect the current milestone, integration sanity, or demo credibility.
4. Keep runtime keys or paths explicit so code, data, and content refer to the same thing.
5. Mark placeholders honestly instead of hiding them behind vague notes.
6. Update it alongside `reports/demo-readiness.md` and `design/gdd/art-bible.md` when the demo contract changes.

## What The Art Bible Is

`design/gdd/art-bible.md` is the shared visual contract for the project.
Use `gamedev/templates/art-bible.md` as the canonical template.

It is the right place to capture:

- visual identity and reference board
- palette and emotional color mapping
- character, environment, UI, and VFX standards
- asset naming and texture rules
- animation expectations such as strip counts, frame rates, or rig rules

It is not:

- a replacement for `docs/technical-preferences.md`
- a system GDD
- a backlog of every asset to make
- a reason to block MVP progress when placeholders are still sufficient

## When To Create The Art Bible

Create or refresh it when one of these becomes true:

- more than one person or tool is producing art
- the team is importing packs, AI outputs, and manual edits that need one visual contract
- `prepare-demo` reveals that placeholder drift is now a credibility problem
- UI, props, characters, and VFX are starting to feel like separate games

For small projects, it does not need to be large.
A short, concrete visual contract is usually better than a bloated lore-heavy art bible.

## How To Use The Art Bible

1. Start from `gamedev/templates/art-bible.md`.
2. Save the project copy as `design/gdd/art-bible.md` by default unless the project has a stronger existing structure.
3. Fill only the sections that reduce ambiguity right now.
4. Use the document to brief artists, external contractors, AI generation passes, or runtime specialists.
5. Update it when the demo contract, readability rules, or asset budgets change.
6. Keep it aligned with `reports/demo-readiness.md` when the placeholder policy changes.

## Three Practical Asset Pipelines

### 1. 2D Pixel Or Sprite Game

Best when:

- the team needs a cheap MVP
- animation must stay readable and deterministic
- the runtime is sprite-friendly

Recommended production pattern:

- approve one in-game seed frame first
- generate or edit a whole strip in one pass, not frame by frame
- normalize frame size, anchor, and scale before import
- keep UI animation separate from sprite animation

Animation default:

- sprite strips for character states
- engine tweens for HUD and menus
- short sheets or code-driven effects for VFX

Codex is useful for:

- prompt shaping
- sprite strip workflow glue
- normalization and import checks
- placeholder policy documentation
- asset registry maintenance when runtime keys or source provenance start drifting

Specialist or MCP depth helps when:

- the team wants consistent 2D strip generation
- Aseprite-like editing or sprite review becomes important
- multiple characters or attack sets must stay visually locked

For browser work, the usual specialist overlay is `sprite-pipeline`.

### 2. 2D Hand-Painted Or UI-Heavy Demo

Best when:

- the next milestone is a pitch build or polished vertical slice
- interface quality and presentation carry a large part of the value
- the team mixes backgrounds, UI, portraits, and lighter gameplay assets

Recommended production pattern:

- create the art bible before broad asset sourcing
- separate gameplay props, backgrounds, portraits, UI, and VFX into different production lanes
- use packs, manual edits, or contractor work for production assets
- use AI mainly for concepts, splash art, portraits, or moodboards, not for every shipped UI element

Animation default:

- tweens and layout motion for UI
- skeletal or cutout animation where possible
- layered particles and screen feedback for VFX

Codex is useful for:

- turning vague art direction into a concise asset contract
- keeping prompts consistent with the art bible
- wiring assets into the repo and checking drift
- tracking must-replace versus acceptable placeholders in the asset registry

Specialist or MCP depth helps when:

- the pipeline depends on Figma, Photoshop-like tooling, or an asset manager
- UI systems and asset revision loops matter more than raw gameplay animation

For browser work, the usual specialist overlay is `game-ui-frontend`.

### 3. 3D Web Or GLB Pipeline

Best when:

- the project is browser-based but wants a stronger production look than simple 2D placeholders
- the runtime already expects GLB or glTF assets
- greybox-first development is acceptable

Recommended production pattern:

- ship greybox proxies first
- move to cleaned source assets only after the playable loop exists
- export GLB or glTF, then optimize and validate before import
- fix pivots, scale, material reuse, collision, and budgets upstream instead of compensating in code

Animation default:

- skeletal animation for characters
- retargeted motion sets where possible
- code-driven or timeline-driven prop motion
- separate UI animation from 3D character animation

Codex is useful for:

- loader integration
- asset indexing
- validation scripts
- project-side import and budget checks
- keeping the registry aligned with what the runtime actually imports

Specialist or MCP depth helps when:

- the team relies on Blender or other DCC tooling
- rigging, retargeting, compression, or texture packaging becomes central

For browser work, the usual specialist overlay is `web-3d-asset-pipeline`.

## Practical Defaults

- If you are solo or very small-team, default to the 2D pixel or sprite path.
- If demo credibility and presentation matter more than deep gameplay animation, default to the 2D hand-painted or UI-heavy path.
- If you already have real 3D pipeline experience and the project is explicitly web 3D, use the GLB path.

## Recommended Prompt Shape

Use a prompt like this when you want Codex to create or refresh the shared visual contract:

```text
Create or update `design/gdd/art-bible.md` from `gamedev/templates/art-bible.md`.
Keep it concise and practical for a small team.
Capture palette, silhouette rules, UI density, VFX direction, animation expectations, asset naming, and which placeholders are acceptable for the next milestone.
Do not turn this into lore or a giant asset backlog.
```

Use a prompt like this when you want Codex to lock concrete asset usage for the current milestone:

```text
Create or update `design/gdd/asset-registry.md` from `gamedev/templates/asset-registry.md`.
Track only the assets that matter for the current milestone.
List runtime keys or paths, placeholder status, source provenance, scene or system coverage, and which assets must be replaced before demo.
Keep it short and operational.
```
