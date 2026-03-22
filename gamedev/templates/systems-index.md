# Systems Index: [Game Title]

**Status**: [Draft | In Review | Approved]  
**Created**: [YYYY-MM-DD]  
**Last Updated**: [YYYY-MM-DD]  
**Source Concept**: `design/gdd/game-concept.md`

## Overview

[Summarize the mechanical scope in one short paragraph. State what the player
does, what must exist for the core loop to run, and what is intentionally out of
scope for MVP.]

## System List

| System | Category | Priority | Status | Design Doc | Depends On |
|--------|----------|----------|--------|------------|------------|
| [Player Controller] | Core | MVP | [Not Started] | `design/gdd/player-controller.md` | [Input, Physics] |
| [Camera] | Core | MVP | [Not Started] | `design/gdd/camera.md` | [Player Controller] |

Use one row per meaningful system. Mark inferred systems with `(inferred)`.

### Category Guide

- `Core`: foundation systems other features rely on
- `Gameplay`: the systems that create the main play experience
- `Progression`: growth, unlocks, or economy layers
- `Persistence`: save state, profile state, settings
- `Presentation`: UI, audio, or other player-facing wrappers
- `Meta`: onboarding, analytics, accessibility, or support layers

### Priority Guide

- `MVP`: required to test whether the core loop is fun
- `Vertical Slice`: required to show one polished slice of the game
- `Expansion`: useful later, but not required for first playable validation

## Dependency Order

List the recommended design order from foundations to wrappers.

1. [System] - [Why it goes first]
2. [System] - depends on [System]
3. [System] - depends on [System, System]

Call out any cycles or risky dependencies explicitly.

## High-Risk Systems

| System | Risk Type | Why It Is Risky | Mitigation |
|--------|-----------|-----------------|------------|
| [Combat] | [Design] | [Balance or feel is unproven] | [Prototype early with a thin vertical slice] |

Keep only systems that can change scope, schedule, or architecture.

## Progress Snapshot

| Metric | Value |
|--------|-------|
| Total systems identified | [N] |
| MVP systems identified | [N] |
| MVP design docs approved | [N] |
| High-risk systems with prototype coverage | [N] |

## Next Steps

- [ ] Review the system list against the current concept and pillars
- [ ] Design MVP systems in dependency order
- [ ] Prototype the highest-risk system early
- [ ] Update this index when a system changes scope or status
