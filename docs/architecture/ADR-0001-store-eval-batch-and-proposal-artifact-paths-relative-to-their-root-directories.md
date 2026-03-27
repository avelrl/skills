# ADR-0001: store eval batch and proposal artifact paths relative to their root directories

## Status

Proposed

## Date

2026-03-27

## Decision Makers

Repository maintainers

## Reverse-Documentation Context (Optional)

- **Source**: `docs/tech-debt-register.md` item `TD-002`, `docs/design/run-evals.md`, `scripts/run_evals.py`, `scripts/judge_evals.py`, and `scripts/eval_common.py`
- **Implementation Status**: not started
- **Confidence Notes**: The current absolute-path writes and reads are confirmed in code. The need for durable artifacts across moving, archiving, or sharing is explicitly stated in `TD-002`. Any expectation of broader cross-machine handoff beyond that documented debt statement is inferred rather than proven from code alone.

## Context

### Problem Statement

The eval harness persists machine-specific absolute paths inside run and proposal metadata. Those values are later read back as if they are stable. As a result, prepared artifacts become fragile when a run batch or proposal directory is moved, archived, restored elsewhere, or shared with another operator.

This decision is needed now because the artifact format is already documented, the debt is open at priority `P1`, and more automation or tests built around the current format will make migration harder later.

### Current State

Confirmed from the current implementation:

- `prepare_batch()` writes absolute paths into `result.json["workspace"]`.
- `prepare_batch()` writes absolute `run_dir`, `workspace`, and `result_file` values into each `batch.json["scenarios"]` entry.
- `prepare_proposal()` writes absolute `baseline_batch`, `baseline_editable_root`, `workspace`, `patch_file`, and `runs.*` values into `proposal.json`.
- `sync_result_file()`, `score_run()`, `finalize_proposal()`, `prepare_proposal_batch()`, and `judge_proposal()` read those stored values directly.
- `write_proposal_decision()` writes an absolute `decision_file` back into `proposal.json`.

Confirmed effects in the current code paths:

- `sync-results` fails if `result.json["workspace"]` no longer exists at the recorded absolute location.
- `judge_evals.py` treats a missing recorded workspace as unavailable and falls back to path checks from `created_or_updated_paths` only.
- `finalize-proposal` and `judge-proposal` trust stored proposal paths directly, so moving a prepared proposal can break later phases even when the proposal tree itself is intact.

Inferred from a narrow repo search rather than proven as a system guarantee:

- `batch.json` appears to be operator-facing today and is not currently machine-read elsewhere in this repository. It is still part of the documented artifact contract and should not keep machine-local path debt.

### Constraints

- The change must stay scoped to artifact path storage and resolution. It must not become a full eval-harness redesign.
- Existing CLI commands and artifact directory layouts should remain intact.
- Existing artifacts with absolute paths must remain readable during migration.
- The metadata should remain easy for humans to inspect during manual eval workflows.
- Resolution must be based on the metadata file location, not on the caller's current working directory.

### Requirements

- A moved batch directory must still contain enough information to resolve its own run-local files.
- A moved proposal directory must still contain enough information to resolve its own proposal-local files.
- A proposal that moves together with its referenced baseline batch in the same relative layout should continue to resolve that baseline reference.
- The harness must accept both legacy absolute values and new relative values during the transition.
- The decision must cover migration concerns for `result.json`, `batch.json`, and `proposal.json`.
- External references that are not necessary to solve this debt should remain out of scope unless they are already part of the affected path set.

## Decision

Store eval artifact paths as relative paths resolved from the directory that owns the metadata file, and update readers to accept both legacy absolute values and new relative values.

### Architecture

```text
run dir/
  result.json  --resolve-from--> run dir root
  workspace/

batch dir/
  batch.json   --resolve-from--> batch dir root
  <run>/...

proposal dir/
  proposal.json --resolve-from--> proposal dir root
  baseline/
  workspace/
  candidate.patch
  runs/
    focused/
    full/
  decision.json

proposal dir/proposal.json
  baseline_batch --relative path--> referenced baseline batch root
  Example: ../runs/<baseline-batch>
```

### Key Interfaces

```python
def resolve_metadata_path(metadata_file: Path, stored_value: str) -> Path:
    candidate = Path(stored_value)
    if candidate.is_absolute():
        return candidate  # legacy format remains readable
    return (metadata_file.parent / candidate).resolve()


def encode_metadata_path(metadata_file: Path, target: Path) -> str:
    owner_root = metadata_file.parent
    return Path(os.path.relpath(target, owner_root)).as_posix()
```

Artifact ownership rules:

- In `result.json`, `workspace` is stored relative to the run directory that contains `result.json`.
- In `batch.json`, each scenario entry stores `run_dir`, `workspace`, and `result_file` relative to the batch directory that contains `batch.json`.
- In `proposal.json`, `baseline_batch`, `baseline_editable_root`, `workspace`, `patch_file`, `runs.focused`, `runs.full`, and `decision_file` are stored relative to the proposal directory that contains `proposal.json`.

Explicit non-goals for this ADR:

- Do not redesign the batch or proposal directory layouts.
- Do not change scenario selection, scoring, or proposal gating.
- Do not require a full artifact schema redesign or field renaming.
- Do not broaden this decision to every path-looking field in the harness. `scenario_file` fallback behavior and `summary.json["batch_dir"]` are out of scope for this ADR.

### Implementation Guidelines

- Keep current field names. Change only how values are encoded and resolved.
- Introduce one shared helper for path decoding so `run_evals.py` and `judge_evals.py` do not drift.
- Writers must emit normalized relative strings for the path fields covered by this ADR.
- Readers must treat absolute values as legacy but valid.
- Relative resolution must always use the metadata file's parent directory as the owner root.
- Proposal-local paths should never be resolved from `REPO_ROOT` or the current working directory.
- `baseline_batch` may resolve outside the proposal directory via `..` segments. That is acceptable because it is still anchored to the proposal directory, not to a machine-specific absolute prefix.

## Alternatives Considered

### Alternative 1: Keep absolute paths and add a repair or rebase command

- **Description**: Preserve the current artifact format and add a helper command that rewrites paths after a move.
- **Pros**: Minimal code churn in current readers. Explicit operator action can repair known-bad artifacts.
- **Cons**: Artifacts remain fragile by default. Sharing and archiving still require an extra recovery step. Operators must remember to repair metadata before follow-up commands work.
- **Estimated Effort**: Low
- **Rejection Reason**: It treats portability as an after-the-fact repair instead of a property of the artifact format.

### Alternative 2: Store paths relative to `REPO_ROOT`

- **Description**: Replace absolute paths with paths relative to the repository root discovered in `scripts/eval_common.py`.
- **Pros**: Simple mental model while artifacts stay inside one checkout. Easy to compute from current code.
- **Cons**: Prepared batches and proposals are still tied to the original repository layout. Archiving or sharing an artifact independently of the original checkout remains brittle.
- **Estimated Effort**: Low to medium
- **Rejection Reason**: The debt is specifically about artifact fragility after moving or sharing prepared outputs. Repo-root-relative paths do not solve that well enough.

### Alternative 3: Stop storing most internal paths and derive them purely from layout conventions

- **Description**: Remove fields like `workspace`, `result_file`, `patch_file`, and `runs.*` where the path could be reconstructed from the known directory structure.
- **Pros**: Less metadata drift. Fewer stored paths to migrate. Stronger coupling to the actual artifact layout.
- **Cons**: More invasive redesign. Some references, especially `baseline_batch`, still need explicit storage. Operator-facing metadata becomes less explicit, and more code paths must be rewritten at once.
- **Estimated Effort**: Medium to high
- **Rejection Reason**: It is broader than the debt item and changes more of the harness contract than needed for this fix.

## Consequences

### Positive

- Prepared batches and proposals become resilient to moves within archives or alternate parent directories, as long as their internal relative structure is preserved.
- Proposal metadata no longer hard-codes machine-local absolute prefixes for proposal-local artifacts.
- The path contract becomes easier to test because it depends on owner-root semantics instead of the original machine path.
- Archived metadata becomes more inspectable as artifact-relative intent instead of host-specific path snapshots.

### Negative

- Every reader of these metadata fields must handle two formats during migration.
- Relative paths that include `..` are less immediately readable than an absolute path, especially for `baseline_batch`.
- Moving a proposal without its referenced baseline batch can still break `judge-proposal`; this ADR improves that dependency by making it relative, but it does not remove the dependency.

### Neutral

- CLI command names and artifact directory layouts do not change.
- Existing JSON field names stay the same.
- The runtime cost of path resolution moves from "none" to "negligible path join and normalize."

## Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| One code path keeps reading raw strings and bypasses the new resolver | Medium | High | Centralize path decoding in one helper and update all known read sites together |
| Mixed old and new artifacts behave inconsistently during rollout | Medium | High | Make readers backward-compatible before writers start emitting relative values |
| Incorrect owner root is used for one file type | Low | High | Document ownership rules in code and add narrow regression tests for each artifact type |
| `baseline_batch` relative paths are misunderstood by operators | Medium | Medium | Document that proposal-relative `..` segments are intentional and expected |

## Performance Implications

| Metric | Before | Expected After | Budget |
|--------|--------|---------------|--------|
| CPU / compute | Negligible | Negligible | No measurable impact expected |
| Memory | Negligible | Negligible | No measurable impact expected |
| Latency / load time | Single direct path parse | Single path parse plus join/normalize | No user-visible impact expected |
| Network (if applicable) | N/A | N/A | N/A |

## Migration Plan

1. Add shared helpers for encoding and resolving metadata paths, and update readers first so both absolute and relative values work.
2. Update all writers for the covered fields in `result.json`, `batch.json`, and `proposal.json` to emit relative values from the correct owner root.
3. Opportunistically rewrite legacy absolute values to relative values whenever an existing artifact is rewritten by normal commands such as `sync-results`, `record-routes`, `finalize-proposal`, or `judge-proposal`.
4. Update the eval design docs to describe owner-root-relative resolution, then close `TD-002` once the migration is implemented and verified.

**Rollback plan**: Revert writers to emit absolute paths again while keeping backward-compatible readers in place. Previously written relative artifacts remain readable because the tolerant reader path stays available.

## Validation Criteria

- [ ] A prepared batch still works after the entire batch directory is moved to a different parent directory, and `sync-results` resolves `workspace/` from `result.json` without manual edits.
- [ ] `judge_evals.py` can score a moved batch using the moved run-local metadata.
- [ ] A prepared proposal still works after the proposal directory moves, and `finalize-proposal` resolves `baseline/`, `workspace/`, and `candidate.patch` from `proposal.json`.
- [ ] A proposal and its baseline batch still work after both are moved together while preserving their relative layout.
- [ ] Legacy artifacts with absolute paths continue to work during the migration window.

## Related

- `docs/tech-debt-register.md`
- `docs/design/run-evals.md`
- `scripts/run_evals.py`
- `scripts/judge_evals.py`
- `scripts/eval_common.py`
