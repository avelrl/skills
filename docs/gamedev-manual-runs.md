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

## Coverage Model

- Core workflow scenarios must stay platform-agnostic.
- Overlay scenarios may use browser fixtures when that is the cheapest reproducible way to exercise specialist handoffs.
- A web fixture is a harness convenience, not a statement that `gamedev/` is browser-only.
- Browser-specialist behavior must not leak back into generic skills unless the rule is truly platform-agnostic.

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

- **Prompt**: `pick the stack for a small top-down action game`
- **Expected start**: `setup-engine`
- **Expected output**: `docs/technical-preferences.md`
- **Bad signs**:
  - jumps into coding
  - creates system docs before stack selection
  - invents implementation files

### 2. Systems Mapping

- **Prompt**: `break the game into systems`
- **Expected start**: `map-systems`
- **Expected output**: `design/gdd/systems-index.md`
- **Typical next step**: `design-system` or `prototype` when the highest-leverage move is risk reduction first
- **Bad signs**:
  - writes a full system GDD immediately
  - skips dependency order
  - does not identify high-risk systems

### 3. Single System Design

- **Prompt**: `write the combat design doc`
- **Expected start**: `design-system`
- **Expected output**: one canonical system GDD
- **Bad signs**:
  - expands into multiple GDDs
  - starts implementing code
  - ignores systems index prerequisites

### 4. Risky Mechanic Check

- **Prompt**: `test the dash mechanic and check whether the combat loop still reads`
- **Expected start**: `prototype`
- **Expected output**: `prototypes/[slug]/REPORT.md`
- **Bad signs**:
  - edits production code
  - skips the report
  - treats the prototype as final implementation

### 5. Project Scaffold

- **Prompt**: `bootstrap the project scaffold`
- **Expected start**: `bootstrap-project`
- **Expected output**: runnable scaffold plus `README.md` guidance
- **Bad signs**:
  - invents systems not yet designed
  - builds too much content
  - ignores `docs/technical-preferences.md`

### 6. Single System Implementation

- **Prompt**: `implement movement`
- **Expected start**: `implement-system`
- **Expected output**: one system implemented in production code
- **Bad signs**:
  - implements unrelated systems
  - silently redesigns the GDD
  - skips status sync in the systems index

### 7. First Playable

- **Prompt**: `assemble the first playable`
- **Expected start**: `assemble-mvp`
- **Expected output**: playable loop plus `reports/mvp-assembly-report.md`
- **Bad signs**:
  - turns into feature implementation marathon
  - cannot explain loop boundaries
  - does not identify blockers and placeholders

### 8. Demo Preparation

- **Prompt**: `plan the first public demo from the current playable`
- **Expected start**: `prepare-demo`
- **Expected output**: `reports/demo-readiness.md`
- **Typical next step**: `design-system` or `implement-system` for the highest-leverage demo-critical system
- **Bad signs**:
  - treats the step as direct UI implementation
  - writes vague polish notes instead of a real demo contract
  - does not name specialist UI, asset, or QA handoffs when they are clearly needed

### 9. Focused Tuning

- **Prompt**: `tune the combat loop`
- **Expected start**: `playtest-and-tune`
- **Expected output**: `reports/playtest-report.md`
- **Bad signs**:
  - adds major new features
  - hides structural gaps with small value changes
  - does not sync tuning back to docs or follow-up path

## Blocked Scenarios

Run these too. They are usually more important than happy paths.

### 10. Implementation Without GDD

- **Prompt**: `implement combat`
- **Missing prerequisite**: system GDD
- **Expected route**: stop and route to `design-system`
- **Typical next step after the missing GDD is written**: `bootstrap-project` if the runnable scaffold is still missing
- **Bad sign**: starts coding anyway

### 11. Assembly Without Enough Systems (Retired)

- This legacy blocked check is no longer part of the active eval suite.
- Reason: the short prompt `assemble a playable` is too ambiguous and overlaps with full-run recovery behavior.
- Use `Blocked Assemble MVP` instead when you want a deterministic blocked step-by-step check for `assemble-mvp`.

### 12. Tuning Without Playable Build

- **Prompt**: `do a playtest pass on the current build`
- **Missing prerequisite**: runnable build
- **Expected route**: stop and route to the nearest real prerequisite such as `implement-system` or `assemble-mvp`
- **Expected output**: no `playtest-and-tune` report yet; only the blocked route and next handoff
- **Bad sign**: invents tuning notes without running anything

## Phase 2 Regression Scenarios

Run these after the baseline set is green.
They are meant to stress overlay behavior, richer runtime paths, and end-result routing.

### 13. Real Playtest Pass

- **Prompt**: `Run a real playtest pass on the current Courier Drift web build...`
- **Fixture**: `playtest_ready_slice`
- **Note**: this is intentionally a browser-overlay scenario, not the definition of the whole workflow
- **Expected start**: `playtest-and-tune`
- **Expected output**: `reports/playtest-report.md`
- **Bad signs**:
  - routes backward even though the playable slice exists
  - writes tuning notes without a real run
  - adds new systems instead of tuning the current loop

### 14. Blocked Assemble MVP

- **Prompt**: `We need the first playable... Perform only the nearest correct workflow step`
- **Fixture**: `scaffold_ready`
- **Mode**: step-by-step blocked-route check, not a full-run recovery prompt
- **Expected route**: stop the fake assembly path and route to `implement-system`
- **Expected output**: no assembly report yet; only the blocked route and next handoff
- **Bad signs**:
  - writes `reports/mvp-assembly-report.md` for a blocked run
  - unlocks the request by silently implementing missing systems first
  - turns the blocked step into a disguised full-run recovery

### 15. Prototype Before Combat Lock

- **Prompt**: `make a disposable prototype and check whether the interceptor telegraph reads clearly`
- **Fixture**: `gdd_ready`
- **Expected start**: `prototype`
- **Expected output**: `prototypes/[slug]/REPORT.md`
- **Typical next step**: another `prototype` if the spike returns `PIVOT`, otherwise `design-system`
- **Bad signs**:
  - edits production code
  - writes a combat implementation instead of a spike
  - skips the documentation follow-up path

### 16. Full-Run Routing From Known Stack

- **Prompt**: `Take this concept to the first MVP`
- **Fixture**: `stack_known`
- **Expected mode**: full-run
- **Expected first route**: `map-systems`
- **Expected output**: `design/gdd/systems-index.md`
- **Bad signs**:
  - jumps straight into scaffold or code
  - skips the systems map even though stack selection is already done
  - silently runs too far downstream without grounding the route first

### 17. Closure Doc Sync Honesty

- **Prompt**: `The current playable slice already exists, but the closure docs disagree with each other...`
- **Fixture**: `closure_sync_needed`
- **Mode**: step-by-step closure-sync check on an already verified slice
- **Expected start**: `playtest-and-tune`
- **Acceptable alternate start**: `assemble-mvp`
- **Expected output**: synced `README.md`, `reports/mvp-assembly-report.md`, `reports/playtest-report.md`, `design/gdd/systems-index.md`, and relevant system GDD status/checklist updates
- **Bad signs**:
  - adds new systems or a fresh feature pass during doc sync
  - turns the request into hidden recovery work instead of honest closure sync
  - leaves contradictory closure state across README, reports, and systems docs
  - leaves stale acceptance criteria unresolved when the current evidence already claims closure

### 18. Closure Repeatability Honesty

- **Prompt**: `The current slice is close to closure, but the repeatability evidence still looks doubtful...`
- **Fixture**: `closure_repeatability_unproven`
- **Mode**: step-by-step closure-state check with mixed success/failure evidence
- **Expected start**: `playtest-and-tune`
- **Acceptable alternate start**: `assemble-mvp`
- **Expected output**: synced `README.md`, `reports/mvp-assembly-report.md`, `reports/playtest-report.md`, and `design/gdd/systems-index.md`
- **Bad signs**:
  - keeps `Stable MVP` purely on the strength of one old success artifact
  - turns the request into feature work or broad retuning
  - downgrades integrated systems as if the runtime loop itself had disappeared
  - ignores the latest failed rerun when describing closure state

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
