# [Slice Name] — MVP Assembly Report

## Status

- **Report Path**: `reports/mvp-assembly-report.md`
- **Date**: [YYYY-MM-DD]
- **Slice**: [Name]
- **Build or Run Target**: [Command, scene, or target]
- **Verification Commands Run**: [Exact commands run or `Blocked by environment: ...`]
- **Assembly State**: [Playable | Partial | Blocked]

## Goal

[State the smallest playable loop this assembly pass was trying to prove.]

## Integrated Systems

| System | Current Role In Loop | Verified In Build? | Notes |
|--------|----------------------|--------------------|-------|
| [Player Movement] | [Traversal / input] | [Yes | Partial | No] | [Short note] |

## Playable Loop

- **Boot flow**: [How the player reaches the loop]
- **Core interaction loop**: [What the player does repeatedly]
- **Objective or pressure**: [What creates momentum]
- **Fail state**: [How a run can end]
- **Restart or exit flow**: [How the loop resets or exits]

## What Works Now

- [Confirmed working path or mechanic]
- [Confirmed working path or mechanic]

## Evidence Artifacts

- [Stable artifact path under `reports/` or another versioned project folder]
- [Or one reproducible verification command if no artifact was kept]

## Missing Glue or Broken Links

- [What still blocks a clean end-to-end run]
- [What still blocks a clean end-to-end run]

## Temporary Stubs or Placeholders

- [Placeholder content, art, data, or logic]
- [Placeholder content, art, data, or logic]

## Systems Index Sync

- **Index Path**: `design/gdd/systems-index.md` or `Not present`
- **Systems moved to `integrated`**: [List or `None`]
- **Status notes**: [Anything that still prevents a stronger status]

## Known Blockers

- [Blocker]
- [Blocker]

## Recommended Next Step

- [Run `/playtest-and-tune [focus-area]`]
- [Run `/prepare-demo [demo-name]` if the next milestone is an audience-facing demo]
- [Or name the system that must return to `/implement-system`]
