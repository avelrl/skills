# [Game Title] — Asset Registry

## Status

- **Document Path**: `design/gdd/asset-registry.md`
- **Version**: 1.0
- **Last Updated**: [Date]
- **Milestone**: [Prototype | MVP | Demo | Release]
- **Owner**: [Name or team]

## Purpose

[State why the project needs a concrete asset contract right now: placeholder control, import sanity, naming consistency, demo readiness, or handoff clarity.]

## Usage Rules

- This file is the concrete asset inventory and integration contract.
- Use `design/gdd/art-bible.md` for the visual language and style rules, not this file.
- Keep entries practical: only track assets that exist, are planned for the current milestone, or are blocking integration.
- Mark placeholder status explicitly instead of pretending an asset is final.

## Naming And Source Rules

- **Naming convention**: [Example: `category_subject_variant.ext`]
- **Runtime key rule**: [How code, data, or content should reference assets]
- **Source of truth**: [Asset folder, content pipeline, DCC export folder, external pack, etc.]
- **Placeholder policy**: [What is allowed to stay temporary for this milestone]

## Asset Inventory

| Asset ID | Class | Runtime Key / Path | Used By | Milestone Need | Status | Source | Notes |
|----------|-------|--------------------|---------|----------------|--------|--------|-------|
| [player-idle] | [sprite / portrait / bg / ui / sfx / music / vfx / model] | [`assets/player/idle.png` or `player_idle`] | [system, scene, or UI] | [MVP | Demo | Later] | [planned | placeholder | integrated | replace-before-demo] | [AI, pack, hand-made, contractor] | [Scale, animation count, or dependency notes] |

## Scene And System Coverage

| Scene / System | Required Assets | Current Gaps | Risk |
|----------------|-----------------|--------------|------|
| [Main Menu] | [logo, bg, button states] | [Missing hover state] | [Low] |
| [Combat Readability] | [telegraph VFX, hit flash, damage popup] | [Telegraph still placeholder] | [High] |

## Import And Validation Notes

- **Expected directory layout**: [Where final runtime-ready files should live]
- **Format expectations**: [PNG / WEBP / GLB / WAV / atlas / sprite strip / JSON companion]
- **Budget notes**: [Texture size, poly budget, animation count, compression, etc.]
- **Reference checks**:
  - [Key or path rule]
  - [Scene, prefab, or data reference rule]
  - [Placeholder naming or suffix rule]

## Replacement Queue

| Asset ID | Why It Must Change | Deadline | Owner | Replacement Trigger |
|----------|--------------------|----------|-------|---------------------|
| [boss-portrait-temp] | [Too low quality for demo close-up] | [Demo] | [Name] | [Before capture build] |

## Open Questions

- [Question]
- [Question]
