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

Some scenarios intentionally allow more than one valid blocked-route or next-step.
When that happens, the machine-readable scenario in `evals/scenarios/` is the source of truth.

Prepared eval workspaces use a repo-local skill bundle:

- `scripts/run_evals.py prepare ...` generates a scenario-local `AGENTS.md`
- active repo skills are copied into `workspace/.codex/skills/`
- shared repo references are linked under `workspace/.codex/support/`

This keeps the scenario project itself lean while still avoiding any dependency on a global `$HOME/.codex`.
Run the manual eval from the prepared `workspace/`, not from the root of this repo.

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
- **Typical next step**: `design-system` or `prototype` when the highest-leverage move is risk reduction first
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
- **Typical next step after the missing GDD is written**: `bootstrap-project` if the runnable scaffold is still missing
- **Bad sign**: starts coding anyway

### 10. Assembly Without Enough Systems

- **Prompt**: `собери playable`
- **Missing prerequisite**: enough implemented systems
- **Expected route**: stop and route to `implement-system`
- **Bad sign**: fakes assembly with placeholders only

### 11. Tuning Without Playable Build

- **Prompt**: `сделай playtest pass`
- **Missing prerequisite**: runnable build
- **Expected route**: stop and route to the nearest real prerequisite such as `implement-system` or `assemble-mvp`
- **Expected output**: no `playtest-and-tune` report yet; only the blocked route and next handoff
- **Bad sign**: invents tuning notes without running anything

## Phase 2 Regression Scenarios

Run these after the baseline set is green.
They are meant to stress the richer web-runtime path and end-result routing.

### 12. Real Playtest Pass

- **Prompt**: `Прогони реальный playtest по текущей веб-сборке Courier Drift...`
- **Fixture**: `playtest_ready_slice`
- **Expected start**: `playtest-and-tune`
- **Expected output**: `reports/playtest-report.md`
- **Bad signs**:
  - routes backward even though the playable slice exists
  - writes tuning notes without a real run
  - adds new systems instead of tuning the current loop

### 13. Blocked Assemble MVP

- **Prompt**: `Нужно собрать первый playable... Выполни только ближайший корректный шаг по workflow`
- **Fixture**: `scaffold_ready`
- **Mode**: step-by-step blocked-route check, not a full-run recovery prompt
- **Expected route**: stop the fake assembly path and route to `implement-system`
- **Expected output**: no assembly report yet; only the blocked route and next handoff
- **Bad signs**:
  - writes `reports/mvp-assembly-report.md` for a blocked run
  - unlocks the request by silently implementing missing systems first
  - turns the blocked step into a disguised full-run recovery

### 14. Prototype Before Combat Lock

- **Prompt**: `сделай disposable prototype и проверь, читается ли телеграф перехватчика`
- **Fixture**: `gdd_ready`
- **Expected start**: `prototype`
- **Expected output**: `prototypes/[slug]/REPORT.md`
- **Typical next step**: another `prototype` if the spike returns `PIVOT`, otherwise `design-system`
- **Bad signs**:
  - edits production code
  - writes a combat implementation instead of a spike
  - skips the documentation follow-up path

### 15. Full-Run Routing From Known Stack

- **Prompt**: `Хочу довести этот концепт до первого web MVP`
- **Fixture**: `stack_known`
- **Expected mode**: full-run
- **Expected first route**: `map-systems`
- **Expected output**: `design/gdd/systems-index.md`
- **Bad signs**:
  - jumps straight into scaffold or code
  - skips the systems map even though stack selection is already done
  - silently runs too far downstream without grounding the route first

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
3. phase 2 regressions after the baseline set is green
4. full-run scenario last

If blocked scenarios fail, do not trust the happy path results.
