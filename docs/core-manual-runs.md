# Core Manual Runs

Use this document for manual evaluation of the active shared `core/` skills.

This is the human runbook.
It exists to answer:

1. What scenarios should we run by hand for shared core skills?
2. What counts as a good or bad result?

## When To Use This

Use manual runs when:

- a shared `core/` skill was added or changed
- repo-level documentation or templates changed
- browser smoke or doctor behavior changed
- a shared skill started drifting into `gamedev/` rules
- the current evidence lives only in one-off chat history

Do manual runs before treating a shared skill as durable infrastructure.

## Coverage Model

- These scenarios are for shared `core/` behavior, not for `gamedev/` flow validation.
- Prefer repo-local, low-friction targets over synthetic playgrounds when the resulting artifact is useful to this repo.
- Browser scenarios may use a tiny local demo when that is the cheapest way to isolate `web-ui-smoke` or `web-ui-doctor`.
- Do not treat indirect use inside a game repo as full validation of a shared core skill when the skill never owned the main artifact.

## Goal

The goal is not to prove that every shared skill works on every repo.

The goal is to verify:

- correct routing
- correct artifact ownership
- correct scope boundaries
- correct failure diagnosis when relevant
- no silent expansion into adjacent skills

## Run Format

For each manual run, record:

- starting repository state
- user prompt
- expected first skill or route
- expected artifact or output
- actual result
- mismatch notes

Unlike `docs/gamedev-manual-runs.md`, these scenarios do not yet have a full machine-readable mirror.
If a scenario later becomes durable enough for `evals/`, this document should stay aligned with that machine-readable source.

## Core Manual Scenarios

### 1. Web UI Smoke Happy Path

- **Prompt**: create a tiny local demo site and verify one happy-path browser flow with screenshots
- **Expected start**: `web-ui-smoke`
- **Expected output**: demo app under a temporary local path plus browser artifacts under `./.codex-artifacts/web-ui/`
- **Bad signs**:
  - installs repo-local Playwright to paper over runtime issues
  - hardcodes global browser executable paths
  - skips screenshots or `summary.json`
  - routes into `web-ui-doctor` even though normal smoke works

### 2. Web UI Doctor Failure Path

- **Prompt**: diagnose why browser verification cannot open `http://127.0.0.1:4173`
- **Expected start**: `web-ui-doctor`
- **Expected output**: exact layer classification plus doctor artifacts under `./.codex-artifacts/web-ui-doctor/`
- **Expected diagnosis shape**:
  - separate bind, reachability, minimal browser launch, and target launch
  - name the exact blocking layer
  - stop after diagnosis instead of converting back into normal smoke
- **Bad signs**:
  - guesses instead of isolating stages
  - edits the repo while “debugging”
  - blames Playwright generically without separating runtime from target reachability

### 3. Reverse-Document Shared Tooling

- **Prompt**: reverse-document `scripts/run_evals.py` into one shared technical design doc
- **Expected start**: `reverse-document`
- **Expected output**: `docs/design/run-evals.md`
- **Bad signs**:
  - writes an ADR instead of a technical design doc
  - invents intent instead of marking inference explicitly
  - rewrites code rather than documenting it

### 4. Shared Tech-Debt Scan

- **Prompt**: scan the repository for high-signal shared technical debt and update the canonical register
- **Expected start**: `tech-debt`
- **Expected output**: `docs/tech-debt-register.md`
- **Bad signs**:
  - turns into a feature backlog
  - logs cosmetic style nits as debt
  - produces a noisy long list without impact or cleanup targets

### 5. Architecture Decision From Existing Debt

- **Prompt**: create one proposed ADR for storing eval artifact paths relative to their owner roots
- **Expected start**: `architecture-decision`
- **Expected output**: one canonical ADR under `docs/architecture/`
- **Bad signs**:
  - writes a general design doc instead of an ADR
  - creates multiple ADRs in one pass
  - changes code while drafting the decision

## Optional Follow-Up Scenarios

Run these after the baseline set is green.

### 6. Reverse-Document the Judge Path

- **Prompt**: reverse-document `scripts/judge_evals.py`
- **Expected start**: `reverse-document`
- **Expected output**: one technical design doc for the judge path
- **Why this matters**: checks whether `reverse-document` still stays narrow on a smaller, scoring-focused target

### 7. Tech-Debt Prioritize or Report

- **Prompt**: reprioritize the current debt register or summarize it for the next cycle
- **Expected start**: `tech-debt`
- **Expected output**: updated `docs/tech-debt-register.md` or a clean inline report, depending on mode
- **Why this matters**: validates that the skill can work from an existing register rather than only bootstrapping one

### 8. Second ADR Pass

- **Prompt**: create one proposed ADR for another concrete repo-level decision
- **Expected start**: `architecture-decision`
- **Expected output**: the next numbered ADR under `docs/architecture/`
- **Why this matters**: checks numbering, template reuse, and boundary discipline on a second pass

## Pass Criteria

A scenario passes when:

- the first route is correct
- the produced artifact is the correct one
- the skill respects its ownership boundary
- the output is grounded in repo facts, not generic filler

## Fail Patterns To Watch

- wrong first skill
- writes the wrong artifact type
- hidden code changes during a documentation-only task
- shared core skill quietly pulling in `gamedev/`-specific doctrine
- browser diagnosis that never identifies the exact failure layer
- debt register noise instead of actionable debt

## Manual Run Report Template

Use this format when logging results:

```md
# Manual Run

- Date:
- Scenario:
- Starting State:
- Prompt:
- Expected Start:
- Expected Output:
- Actual Result:
- Pass / Fail:
- Mismatch Notes:
```
