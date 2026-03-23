# Systems Index: [Game Title]

**Status**: [Draft | In Review | Approved | Living]
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
| [Player Controller] | Core | MVP | [identified] | `design/gdd/player-controller.md` | [Input, Physics] |
| [Camera] | Core | MVP | [identified] | `design/gdd/camera.md` | [Player Controller] |

Use one row per meaningful system. Mark inferred systems with `(inferred)`.
Choose the strongest confirmed status that is true for each system. Do not
downgrade a row during refresh; only move it forward when new evidence exists.

### Status Guide

- `identified`: listed in the systems map only
- `designed`: canonical GDD exists for the system
- `prototyped`: a relevant `prototypes/[slug]/REPORT.md` exists, but its findings are not fully folded into the canonical docs
- `informed-by-prototype`: prototype findings and baseline decisions are reflected in the GDD or systems index
- `implemented`: production code exists for the system
- `integrated`: the implementation is wired into the main playable loop or production flow

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

| System | Risk Type | Why It Is Risky | Mitigation | Prototype Candidate | Evidence Needed |
|--------|-----------|-----------------|------------|---------------------|-----------------|
| [Combat] | [Design] | [Balance or feel is unproven] | [Prototype early with a thin vertical slice] | [`/prototype melee-time-to-kill`] | [Readable telegraphs, stable damage baseline] |

Keep only systems that can change scope, schedule, or architecture.
List only real MVP risks; if only two exist, list two instead of padding.

## Progress Snapshot

| Metric | Value |
|--------|-------|
| Total systems identified | [N] |
| MVP systems identified | [N] |
| Systems with canonical GDDs | [N] |
| Systems with prototype evidence adopted | [N] |
| High-risk systems without evidence coverage | [N] |

## Next Steps

- [ ] Review the system list against the current concept and pillars
- [ ] Design MVP systems in dependency order
- [ ] Prototype the highest-risk system early
- [ ] Fold prototype findings back into the relevant GDDs and status rows
- [ ] Update this index when a system changes scope or status
