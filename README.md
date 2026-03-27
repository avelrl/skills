# my_skills

Small local skill and template library with one active domain package: `gamedev/`.

`AGENTS.md` stays the routing source of truth.
This README is the high-level entrypoint: repo map, current validation status, and the next test plan.

## Repo Map

- `core/`: shared workflows that still make sense without `gamedev/`
- `gamedev/`: game-specific skills, standards, templates, and active workflow
- `docs/`: repository guidance and explanatory docs
- `templates/`: shared skeletons
- `standards/`: compact shared conventions
- `productivity/`: optional helper utilities
- `evals/`: machine-readable scenarios and regression harnesses
- `fixtures/`: prepared repo states for manual and eval checks

## Read Order

1. `AGENTS.md`
2. `docs/context-management.md` when the task spans multiple edits or docs
3. `docs/gamedev-workflow.md` for the canonical game flow
4. `docs/gamedev-specialist-handoffs.md` for runtime-, engine-, UI-, asset-, and QA-specific overlays

## Validation Snapshot

Current manual validation has focused on `gamedev/`, browser-game overlays, one non-browser desktop lane, and the blocked-routing layer of the active workflow.

- Strongest confirmed lane: small 2D browser full-run to honest `Stable MVP`
- Also confirmed lane: 3D browser full-run to `Stable MVP` after repeatable browser-smoke closure
- Newly confirmed lane: desktop Pygame full-run to honest `Stable MVP` on a repo-local conda environment
- Newly confirmed behavior: blocked step-by-step routing across three core prereq scenarios
- Newly confirmed behavior: deliberate `web-ui-doctor` failure-path diagnosis with exact layer classification
- Biggest remaining gaps: reusable regression fixtures for the strongest manual runs and a clearer manual-run story for shared `core/` skills as a group

Status labels below are intentionally rough:

- `checked`: exercised in at least one real manual run
- `partial`: touched, but still has an unresolved gap or weak evidence
- `not checked`: not yet validated in a meaningful run

## Coverage Table

| Area / Skill | Status | Evidence | Remaining gap |
| --- | --- | --- | --- |
| `gamedev/setup-engine` | checked | 2D and 3D full-runs selected a stack and produced `docs/technical-preferences.md` | none critical |
| `gamedev/map-systems` | checked | systems maps and risk rows were created and maintained in real repos | none critical |
| `gamedev/design-system` | checked | canonical GDDs were created, revised, and re-synced in browser and non-browser repos | none critical |
| `gamedev/prototype` | checked | risky mechanic spikes were used and folded back into docs in browser and Pygame runs | none critical |
| `gamedev/bootstrap-project` | checked | runnable browser and non-browser scaffolds were produced | none critical |
| `gamedev/implement-system` | checked | system-by-system production changes were exercised in both lanes | none critical |
| `gamedev/assemble-mvp` | checked | browser and non-browser loops were assembled and pushed through closure reports | none critical |
| `gamedev/playtest-and-tune` | checked | real tuning passes happened with evidence, doc sync, and closure in browser and non-browser repos | none critical |
| Blocked step-by-step routing from `docs/gamedev-manual-runs.md` | checked | `implement_without_gdd`, `blocked_assemble_mvp`, and `tuning_without_build` all routed to the nearest prerequisite without hidden recovery | broader blocked matrix still worth growing later |
| Specialist handoff rules in `docs/gamedev-specialist-handoffs.md` | checked | browser-specific depth stayed in specialist overlays while the Pygame run stayed generic | none critical |
| Browser 2D overlay (`Game Studio` + Phaser lane) | checked | strongest current lane; reached honest `Stable MVP` | none critical |
| Browser 3D overlay (`Game Studio` + Three.js lane) | checked | reached `Stable MVP` with saved repeatable browser-smoke evidence | opening readability polish remains, but it is not a closure blocker |
| `core/web-ui-smoke` | checked | used repeatedly in browser repos and also exercised directly on a small local demo | dedicated negative-case matrix still worth adding later |
| `core/web-ui-doctor` | checked | dedicated deliberate failure-path run separated sandbox bind/connect failures from host-side `ERR_CONNECTION_REFUSED` | broader failure matrix still worth adding later |
| `core/architecture-decision` | checked | isolated ADR pass produced `docs/architecture/ADR-0001-store-eval-batch-and-proposal-artifact-paths-relative-to-their-root-directories.md` without code edits | another ADR later would strengthen coverage breadth |
| `core/reverse-document` | checked | dedicated reverse-document pass produced `docs/design/run-evals.md` from `scripts/run_evals.py` without code edits | another target later would strengthen coverage breadth |
| `core/tech-debt` | checked | dedicated scan pass produced `docs/tech-debt-register.md` with four prioritized repo-level debt items | another scan on a larger repo would strengthen coverage breadth |
| Late asset health check | partial | health-check style pass exists | real asset-pipeline validation still missing |
| Late localization health check | partial | health-check style pass exists | real localization-table workflow still missing |
| Platform-agnostic non-browser `gamedev/` claim | checked | desktop Pygame full-run reached honest `Stable MVP` with repo-native smoke and tests | none critical |

## Where Next

The browser, non-browser, and first blocked-routing lanes are good enough for now.
The next useful information will not come from building another MVP repo of the same kind.

Priority order:

1. Turn the strongest manual runs into reusable regression fixtures or scenarios.
2. Decide whether the shared `core/` skills need their own manual-run doc instead of living only under the gamedev runbook.
3. Turn the new core docs into reusable review or regression targets.

De-prioritized for now:

- another browser polish pass
- visual refinement work
- more late-stage tuning on already playable browser repos
- asset or localization pipeline work without a repo that truly needs it

## Test Plan

### Immediate

1. Convert the strongest browser and non-browser manual runs into reusable fixtures or `evals/` scenarios.
   Goal: preserve the current coverage without re-running the same manual loops from scratch.
2. Decide whether `core/architecture-decision`, `core/reverse-document`, and `core/tech-debt` need a separate `docs/core-manual-runs.md`.
   Goal: avoid pretending the gamedev runbook covers the whole shared-core library.
3. Turn the new core artifacts into reusable review or regression targets.
   Goal: keep this first-pass core coverage from becoming one-off manual evidence.

### Next

1. Add one regression scenario that exercises late doc-sync and closure honesty.
2. Re-check browser or non-browser lanes only if routing or evidence contracts change again.
3. Add one more non-browser engine only if the platform-agnostic claim becomes doubtful again.

### Later

1. Add one real asset-pipeline validation pass once a repo actually ships file-based assets.
2. Add one real localization-table validation pass once a repo stops being English-only.
3. Revisit opening-readability polish only after blocked-routing and failure-path coverage are no longer missing.

## Stop Rules

- Do not spend more than one additional narrow pass on the same repo once the core claim has already been validated.
- If a browser smoke run hangs for several minutes without producing fresh artifacts, stop it and classify the attempt as failed.
- Do not treat a single lucky browser success as durable evidence when repeatability is the actual question.
- Prefer covering an untested claim over polishing an already-validated lane.

## Useful Docs

- `AGENTS.md`
- `docs/gamedev-workflow.md`
- `docs/gamedev-specialist-handoffs.md`
- `docs/gamedev-manual-runs.md`
- `docs/gamedev-autoimprovement.md`
