# Gamedev Manual Runs

Use this document for manual evaluation of the active `gamedev/` skills.

This is the human runbook.
It exists to answer:

1. What scenarios should we run by hand?
2. What counts as a good or bad result?

## When To Use This

Use manual runs when:

- new skills were added
- workflow routing changed
- handoff rules changed
- output templates changed
- the agent started choosing the wrong next step

Do manual runs before building auto-improvement loops.
The current Phase 1 fixtures default to a lightweight web runtime so the harness does not assume Godot or any other specific engine.

## Goal

The goal is not to prove that the agent can finish a whole game.

The goal is to verify:

- correct routing
- correct prerequisite detection
- correct artifact creation
- correct handoff to the next skill
- no silent scope creep

## Run Format

For each manual run, record:

- starting repository state
- user prompt
- expected first skill or route
- expected artifact or output
- actual result
- mismatch notes

## Core Manual Scenarios

These are the baseline scenarios.
Their machine-readable mirror lives under `evals/scenarios/`.

### 1. Stack Selection

- **Prompt**: `подбери стек для небольшой браузерной игры`
- **Expected start**: `setup-engine`
- **Expected output**: `docs/technical-preferences.md`
- **Bad signs**:
  - jumps into coding
  - creates system docs before stack selection
  - invents implementation files

### 2. Systems Mapping

- **Prompt**: `разложи игру по системам`
- **Expected start**: `map-systems`
- **Expected output**: `design/gdd/systems-index.md`
- **Bad signs**:
  - writes a full system GDD immediately
  - skips dependency order
  - does not identify high-risk systems

### 3. Single System Design

- **Prompt**: `сделай диздок боёвки`
- **Expected start**: `design-system`
- **Expected output**: one canonical system GDD
- **Bad signs**:
  - expands into multiple GDDs
  - starts implementing code
  - ignores systems index prerequisites

### 4. Risky Mechanic Check

- **Prompt**: `проверь механику рывка, не развалится ли бой`
- **Expected start**: `prototype`
- **Expected output**: `prototypes/[slug]/REPORT.md`
- **Bad signs**:
  - edits production code
  - skips the report
  - treats the prototype as final implementation

### 5. Project Scaffold

- **Prompt**: `собери каркас проекта`
- **Expected start**: `bootstrap-project`
- **Expected output**: runnable scaffold plus `README.md` guidance
- **Bad signs**:
  - invents systems not yet designed
  - builds too much content
  - ignores `docs/technical-preferences.md`

### 6. Single System Implementation

- **Prompt**: `реализуй movement`
- **Expected start**: `implement-system`
- **Expected output**: one system implemented in production code
- **Bad signs**:
  - implements unrelated systems
  - silently redesigns the GDD
  - skips status sync in the systems index

### 7. First Playable

- **Prompt**: `собери первый playable`
- **Expected start**: `assemble-mvp`
- **Expected output**: playable loop plus `reports/mvp-assembly-report.md`
- **Bad signs**:
  - turns into feature implementation marathon
  - cannot explain loop boundaries
  - does not identify blockers and placeholders

### 8. Focused Tuning

- **Prompt**: `сделай тюнинг боёвки`
- **Expected start**: `playtest-and-tune`
- **Expected output**: `reports/playtest-report.md`
- **Bad signs**:
  - adds major new features
  - hides structural gaps with small value changes
  - does not sync tuning back to docs or follow-up path

## Blocked Scenarios

Run these too. They are usually more important than happy paths.

### 9. Implementation Without GDD

- **Prompt**: `реализуй combat`
- **Missing prerequisite**: system GDD
- **Expected route**: stop and route to `design-system`
- **Bad sign**: starts coding anyway

### 10. Assembly Without Enough Systems

- **Prompt**: `собери playable`
- **Missing prerequisite**: enough implemented systems
- **Expected route**: stop and route to `implement-system`
- **Bad sign**: fakes assembly with placeholders only

### 11. Tuning Without Playable Build

- **Prompt**: `сделай playtest pass`
- **Missing prerequisite**: runnable build
- **Expected route**: stop and route to `assemble-mvp` or `implement-system`
- **Bad sign**: invents tuning notes without running anything

## Pass Criteria

A scenario passes when:

- the first route is correct
- the produced artifact is the correct one
- the agent respects scope boundaries
- the next recommended skill is sensible

## Fail Patterns To Watch

- wrong first skill
- skipped prerequisite
- hidden multi-step run in a step-by-step request
- artifact missing
- wrong artifact path
- stale systems-index status
- prototype treated as production code

## Manual Run Report Template

Use this format when logging results:

```md
# Manual Run

- Date:
- Scenario:
- Starting State:
- Prompt:
- Expected Start:
- Actual Start:
- Expected Output:
- Actual Output:
- Result: Pass / Fail / Mixed
- Notes:
- Follow-Up:
```

## Recommended Order

Run in this order when validating a new revision:

1. blocked scenarios first
2. core happy paths next
3. full-run scenario last

If blocked scenarios fail, do not trust the happy path results.
