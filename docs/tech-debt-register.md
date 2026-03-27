# Tech Debt Register

Canonical shared register for repo-level technical debt with current maintenance, reliability, or delivery cost.

## Scope

- Last scan: 2026-03-27
- Scan focus: `scripts/`, `evals/`, `fixtures/`, `docs/`, and shared eval-harness plumbing
- Excludes feature backlog items, cosmetic nits, and speculative architecture opinions without a concrete cleanup seam

## Current Priorities

| Priority | ID | Category | Area | Debt | Impact | Cleanup target |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | TD-001 | documentation | eval harness docs and proposal mode | Support-doc exposure and proposal edit scope are duplicated across code and docs and have already drifted. | Operators can follow the docs and still hit out-of-scope proposal failures or stale support-path references inside prepared workspaces. | Move support-doc and editable-doc scope into one manifest, then generate or validate both code lists and docs from it. |
| P1 | TD-002 | architecture | eval run and proposal artifacts | Run metadata persists absolute machine paths instead of portable relative paths. | Moving, archiving, or sharing prepared batches can break `sync-results`, `finalize-proposal`, and `judge-proposal`. | Store artifact paths relative to the batch or proposal root and resolve them at runtime. |
| P2 | TD-003 | tests | eval harness scripts | The runner and judge flow have no direct automated regression coverage. | Refactors to scenario loading, diff syncing, proposal validation, or score comparison depend on manual reruns to catch breakage. | Add narrow script-level tests around scenario parsing, result sync, proposal scope validation, and summary comparison. |
| P2 | TD-004 | tests | eval fixtures | Fixture variants are maintained as full-copy snapshots instead of layered bases or generated overlays. | Shared scaffold or workflow changes require manual sync across several near-duplicate fixture trees, which raises drift risk and update cost. | Collapse near-duplicate fixtures into base trees plus overlays, or generate them from a small fixture builder. |

## Active Items

### TD-001: Proposal and support-doc scope have drifted

- Priority: P1
- Category: documentation
- Status: open
- Area: `scripts/run_evals.py`, `docs/gamedev-workflow.md`, `docs/gamedev-autoimprovement.md`, `docs/design/run-evals.md`

Why this is debt:

- `scripts/run_evals.py` hard-codes proposal edit scope in `PROPOSAL_EDITABLE_SETS`, but that list omits `docs/gamedev-specialist-handoffs.md`.
- `docs/gamedev-autoimprovement.md` lists `docs/gamedev-specialist-handoffs.md` as an allowed proposal write target in the safety boundaries.
- `docs/gamedev-workflow.md` treats `docs/gamedev-specialist-handoffs.md` as canonical related guidance.
- `scripts/run_evals.py` also hard-codes support-path rewrites in `SKILL_TEXT_REWRITE_RULES`, and that rewrite set omits `docs/gamedev-specialist-handoffs.md` even though the support bundle copies `docs/`.

Impact:

- Proposal mode cannot cleanly evaluate edits to a documented in-scope workflow doc.
- Prepared eval workspaces can retain repo-root doc references where the local `.codex/support/docs/` path should be the stable target.
- Any future doc-scope change now requires synchronized edits in multiple code constants and docs.

Cleanup target:

- Create one manifest for support docs and editable docs.
- Decide explicitly whether `docs/gamedev-specialist-handoffs.md` is in scope for proposal mode.
- Derive rewrite targets, editable patterns, and operator docs from that manifest or add a consistency check that fails when they diverge.

Evidence:

- `scripts/run_evals.py:28-37`
- `scripts/run_evals.py:74-81`
- `scripts/run_evals.py:642-661`
- `docs/gamedev-workflow.md:5-10`
- `docs/gamedev-workflow.md:151-160`
- `docs/gamedev-autoimprovement.md:177-184`
- `docs/design/run-evals.md:286-292`

### TD-002: Eval artifacts are not portable because metadata stores absolute paths

- Priority: P1
- Category: architecture
- Status: open
- Area: `scripts/run_evals.py`, `scripts/judge_evals.py`

Why this is debt:

- `prepare_batch()` writes absolute resolved paths into `result.json` and `batch.json`.
- `prepare-proposal()` writes absolute resolved paths for the baseline snapshot, proposal workspace, patch file, and rerun batches into `proposal.json`.
- Later commands trust those stored absolute paths instead of resolving from the current artifact location.

Impact:

- Prepared runs and proposals are tied to the original machine path.
- Moving a batch directory, restoring it from an archive, or sharing it with another operator can make follow-up commands fail even when the files are still intact.
- The artifact format is harder to keep durable over time because path semantics are implicit and machine-local.

Cleanup target:

- Store only relative paths inside `result.json`, `batch.json`, and `proposal.json`.
- Resolve them relative to the containing batch or proposal directory at command runtime.
- Add a small schema version or migration path before changing artifact format.

Evidence:

- `scripts/run_evals.py:463-479`
- `scripts/run_evals.py:563-592`
- `scripts/run_evals.py:753-767`
- `scripts/run_evals.py:782-788`

### TD-003: The eval harness has no direct automated regression tests

- Priority: P2
- Category: tests
- Status: open
- Area: `scripts/`, `evals/`, eval proposal flow

Why this is debt:

- The core harness lives in `scripts/run_evals.py` and `scripts/judge_evals.py`, but there are no dedicated tests for those scripts in the repo.
- `scripts/run_evals.py` is already large enough to contain multiple behaviors and edge cases in one file.
- Current test presence in the scanned area is limited to fixture-level checks such as `fixtures/scaffold_ready/tests/game-manifest.test.mjs`, which validate a sample scaffold rather than the harness itself.

Impact:

- Changes to route requirements, diff syncing, proposal validation, or summary comparison can regress silently until someone does a full manual rerun.
- The proposal workflow is especially exposed because it spans prepare, finalize, and judge phases with persistent JSON metadata between steps.

Cleanup target:

- Add script-level tests for scenario loading and required-field validation.
- Add script-level tests for `detect_created_or_updated_paths()` ignore behavior.
- Add script-level tests for proposal editable-scope validation.
- Add script-level tests for summary comparison regression/improvement decisions.
- Keep the first pass narrow and deterministic; do not wait for a full end-to-end browser or agent harness.

Evidence:

- `scripts/run_evals.py` is 1160 lines
- `scripts/judge_evals.py` is 281 lines
- `scripts/eval_common.py` is 92 lines
- `fixtures/scaffold_ready/tests/game-manifest.test.mjs`

### TD-004: Fixture maintenance cost is inflated by near-duplicate snapshot trees

- Priority: P2
- Category: tests
- Status: open
- Area: `fixtures/`

Why this is debt:

- Several fixtures are whole-project snapshots of adjacent workflow states instead of small deltas over a shared base.
- `fixtures/implemented_core_pair` and `fixtures/playtest_ready_slice` differ in only a small subset of files, but both carry full copied project trees.
- `fixtures/scaffold_only` and `fixtures/scaffold_ready` also model closely related states with duplicated docs and scaffold structure.

Impact:

- Updating shared scaffold defaults, docs expectations, or repo conventions requires touching multiple fixture trees by hand.
- Drift between scenarios becomes more likely because one fixture can keep an older README, systems index, or entrypoint while another is updated.
- Adding more scenarios will increase storage and maintenance cost faster than the actual state differences justify.

Cleanup target:

- Define a small set of base fixtures for concept-only, scaffolded, implemented, and playable states.
- Represent scenario-specific differences as overlays or generate fixtures from a fixture builder script.
- Keep only the scenario-relevant delta in each derived fixture.

Evidence:

- `fixtures/implemented_core_pair` has 18 files and is 76K
- `fixtures/playtest_ready_slice` has 19 files and is 92K
- `git diff --no-index --stat fixtures/implemented_core_pair fixtures/playtest_ready_slice` shows only 5 files changed
- `fixtures/scaffold_ready` is 72K versus `fixtures/scaffold_only` at 24K while both represent adjacent scaffold states

## Recommended Next Cleanup Target

Start with TD-001. It is the smallest high-impact fix: one scope alignment pass can remove current doc/code contradictions, unblock proposal-mode edits for the intended workflow surface, and reduce future drift in the eval harness.
