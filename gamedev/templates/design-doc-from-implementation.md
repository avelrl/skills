# [System Name] — Reverse-Documented Design

**Status**: [Reverse-Documented | Verified | Needs Follow-Up]  
**Source**: `[path/to/implementation]`  
**Date**: [YYYY-MM-DD]  
**Verified By**: [Name | Pending Review]  
**Implementation Status**: [Implemented | Partial | Diverged]

Use this when code exists first and the document must capture current behavior,
design intent, and known gaps.

## Overview

**Purpose**: [What problem this system solves]  
**Scope**: [What is included and excluded]  
**Current Behavior**: [Short summary of what the code does today]

## Core Mechanics

List the implemented mechanics in player-facing language, then map them to code.

| Mechanic | Player-Facing Behavior | Implementation Notes | Design Intent |
|----------|------------------------|----------------------|---------------|
| [Primary Action] | [What the player experiences] | `[Key classes/functions]` | [Why this exists] |

## Rules and Data

### Rules or Formulas

| Rule | Current Implementation | Verified? | Follow-Up |
|------|------------------------|-----------|-----------|
| [Damage Formula] | `[expression or description]` | [Yes | No] | [Retune, keep, replace] |

### State and Data

- **Runtime state**: [Key state the system owns]
- **Persistent data**: [What is saved or loaded]
- **Config/data files**: [External tables, configs, or scriptable data]

## Integrations

- **Depends on**: [Systems or services this system needs]
- **Used by**: [Systems that consume this one]
- **Public surface**: [Main entry points, events, or commands]

## Edge Cases and Gaps

- **Handled**: [Known edge case already covered]
- **Unclear**: [Behavior that needs confirmation]
- **Missing**: [Behavior that should exist but does not]

## Acceptance Snapshot

- **Implemented and acceptable**
  - [Criterion]
- **Implemented but risky**
  - [Criterion]
- **Not implemented**
  - [Criterion]

## Open Questions

1. [Question that affects design intent or implementation direction]
2. [Question about balance, state ownership, or dependencies]

## Follow-Up Work

- [ ] [Document a technical decision if the current shape is intentional]
- [ ] [Fix or extend behavior that does not match intent]
- [ ] [Run a focused balance or gameplay validation pass]

## Change Log

| Date | Author | Change |
|------|--------|--------|
| [YYYY-MM-DD] | [Name] | [Initial reverse-documentation] |
