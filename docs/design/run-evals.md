# Technical Design: Eval Scenario Runner and Proposal Workflow

## Document Status
- **Version**: Reverse-documented from current implementation
- **Last Updated**: 2026-03-27
- **Author**: Codex
- **Reviewer**: Unassigned
- **Related ADR**: None
- **Related Product/Design Doc**: None

## Reverse-Documentation Context
This document is reverse-documented from the current implementation in `scripts/run_evals.py`. Narrow supporting reads were limited to `scripts/eval_common.py`, the `missing_result_fields` and `judge_batch` paths in `scripts/judge_evals.py`, and the current scenario files under `evals/scenarios/`.

The document records implementation facts only. Where the code does not prove rationale or intent, the relevant point is marked as inferred or unresolved.

## Overview
`scripts/run_evals.py` is a command-line utility that prepares manual eval workspaces, updates run metadata after those evals, and manages an isolated proposal workflow that can prepare focused and full rerun batches for comparison against a baseline batch summary.

The script does not execute the agent or the manual eval itself. It prepares workspace trees, writes prompts and metadata files, and coordinates with `scripts/judge_evals.py` when a batch is ready to be scored.

## Purpose and Supported Commands

### Observed Purpose
- Materialize one or more scenario-specific workspaces from `fixtures/`.
- Capture and refresh per-run metadata in `result.json`.
- Record actual route choices taken during a manual run.
- Prepare a restricted proposal workspace, generate a candidate patch, and compare rerun results to a baseline batch.

### Supported Commands
| Command | Observed behavior | Primary outputs |
| --- | --- | --- |
| `list` | Loads scenario JSON files and prints scenario name, fixture, expected first route, and prompt. | Console output only |
| `prepare` | Creates a batch directory containing one run directory per selected scenario. | `batch.json`, `prompt.txt`, `result.json`, `scenario.snapshot.json`, `instructions.txt`, `workspace/` |
| `sync-results` | Recomputes `created_or_updated_paths` by diffing a run workspace against its source fixture. | Updated `result.json` |
| `record-routes` | Writes `actual_first_route`, optionally `actual_next_recommendation`, and optionally replaces `notes`. | Updated `result.json` |
| `prepare-proposal` | Creates an isolated editable workspace plus metadata for a proposal experiment. | `proposal.json`, `instructions.txt`, `baseline/`, `workspace/` |
| `finalize-proposal` | Validates the editable workspace and writes `candidate.patch`. Resets prior proposal run artifacts. | Updated `proposal.json`, `candidate.patch` |
| `judge-proposal` | Prepares focused/full rerun batches as needed, waits for manual completion, and writes a comparison decision. | Proposal rerun batches, updated `proposal.json`, `decision.json`, and sometimes `summary.json` via `judge_evals.py` |

## Inputs and Outputs

### Inputs
| Input | Source | Notes |
| --- | --- | --- |
| Scenario definitions | `evals/scenarios/*.json` by default | Loaded through `Scenario.from_path()` in `scripts/eval_common.py` |
| Fixture trees | `fixtures/<fixture>/` by default | Copied into each prepared run workspace |
| Repo skill/support content | `core/`, `gamedev/`, `productivity/`, `templates/`, `standards/`, `docs/` | Injected into `.codex/` unless `--no-local-skills` is set |
| Existing run metadata | `result.json` | Used by `sync-results` and `record-routes` |
| Baseline batch summary | `<baseline-batch>/summary.json` | Required by `prepare-proposal` and `judge-proposal` |
| Proposal overlay content | `<proposal>/workspace/` | Used only when preparing proposal rerun batches |

### Scenario Schema Used by `run_evals.py`
The script relies on the `Scenario` dataclass in `scripts/eval_common.py`. Observed fields are:

- `name`
- `fixture`
- `mode`
- `prompt`
- `expected_first_route`
- `acceptable_first_routes`
- `expected_next_recommendation`
- `acceptable_next_recommendations`
- `expected_paths`
- `expected_globs`
- `forbidden_behaviors`
- `source_path`

Implementation constraint: `Scenario.from_path()` requires `name`, `fixture`, `mode`, and `prompt`, and it also requires at least one first-route expectation (`expected_first_route` or `acceptable_first_routes`).

### Outputs
| Output | Producer | Observed contents |
| --- | --- | --- |
| `batch.json` | `prepare_batch()` | Batch name, UTC preparation time, and per-scenario run metadata |
| `prompt.txt` | `prepare_batch()` | Scenario prompt with trailing newline |
| `result.json` | `prepare_batch()` and later update commands | Scenario identity, workspace path, prompt, actual route fields, changed paths, forbidden hits, notes |
| `scenario.snapshot.json` | `prepare_batch()` | Snapshot of scenario JSON as loaded |
| `instructions.txt` | `prepare_batch()` and `prepare-proposal()` | Human-oriented workflow instructions |
| `.codex/support/` | `install_support_bundle()` | Snapshot of selected repo directories, with text references rewritten |
| `.codex/skills/` | `install_skill_wrappers()` | Local skill wrappers copied from repo `SKILL.md` directories |
| `proposal.json` | `prepare-proposal()`, `finalize-proposal()`, `judge-proposal()` | Proposal metadata, status, paths, scenario lists, changed paths |
| `candidate.patch` | `finalize-proposal()` | Unified diff between proposal `baseline/` and `workspace/` |
| `decision.json` | `judge-proposal()` | Focused/full comparison status and next action |
| `summary.json` | `judge_evals.py` invoked by `ensure_batch_summary()` | Batch scoring summary when a rerun batch is ready |

## Workspace and Batch Layout Assumptions

### Default Roots
Observed default paths are defined in `scripts/eval_common.py`:

- Scenarios: `evals/scenarios/`
- Fixtures: `fixtures/`
- Run batches: `reports/evals/runs/`
- Proposal workspaces: `reports/evals/proposals/`

### Run Batch Layout
`prepare` creates a batch directory at `<out-root>/<batch-name>/`. If `--batch-name` is not provided, the batch name is a UTC timestamp in `YYYYMMDDTHHMMSSZ` format.

Each selected scenario gets a run directory:

```text
<batch-dir>/
  batch.json
  <scenario-name-with-spaces-replaced-by-underscores>/
    instructions.txt
    prompt.txt
    result.json
    scenario.snapshot.json
    workspace/
```

Observed behavior:

- `workspace/` starts as a copy of `fixtures/<scenario.fixture>/`.
- `result.json["workspace"]` stores an absolute resolved path to `workspace/`.
- `scenario.snapshot.json` stores the loaded scenario payload at prepare time.

### Workspace Injection Layout
Unless `--no-local-skills` is set, the script removes any existing `.codex/` directory in the copied workspace and recreates:

```text
workspace/
  AGENTS.md
  .codex/
    support/
      core/
      gamedev/
      productivity/
      templates/
      standards/
      docs/
    skills/
      <skill-leaf-name>/
        SKILL.md
```

Observed behavior:

- `AGENTS.md` is written by the harness and contains eval-specific instructions.
- `discover_repo_skill_dirs()` scans `core/`, `gamedev/`, and `productivity/` for `SKILL.md`, skipping any path that contains `_archive`.
- Skill wrappers are flattened by leaf directory name (`source_skill_dir.name`), not by full relative path.
- Support content is copied from repo root into `.codex/support/`.
- Text files under the support bundle and skill wrappers have selected path references rewritten to `.codex/support/...`.

## Architecture

### System Diagram
```text
scenario JSON + fixture tree
        |
        v
  run_evals.py parser
        |
        +--> prepare ------------------------------+
        |                                          |
        |                                   batch/<scenario>/
        |                                   - workspace/
        |                                   - prompt.txt
        |                                   - result.json
        |                                   - instructions.txt
        |
        +--> sync-results --> fixture/workspace diff --> result.json
        |
        +--> record-routes -------------------------> result.json
        |
        +--> prepare-proposal --> proposal.json + sparse baseline/workspace
        |
        +--> finalize-proposal --> candidate.patch
        |
        +--> judge-proposal --> prepare rerun batches as needed
                                   |
                                   v
                             judge_evals.py
                                   |
                                   v
                        summary.json / decision.json
```

### Component Breakdown
| Component | Responsibility | Owns |
| --- | --- | --- |
| CLI parser | Defines subcommands and options. | Argument surface |
| Scenario loaders | Load scenario metadata and default roots. | `Scenario` contract, root paths |
| Batch preparer | Copies fixtures and writes run metadata files. | Run directory contents |
| Skill/support injector | Builds `.codex/` support snapshot inside prepared workspaces. | `workspace/AGENTS.md`, `.codex/support/`, `.codex/skills/` |
| Result sync path | Recomputes changed file list from fixture/workspace comparison. | `result.json["created_or_updated_paths"]` |
| Route recorder | Writes actual route metadata and optional notes. | `result.json["actual_*"]`, `notes` |
| Proposal preparer | Creates sparse editable proposal trees and metadata. | `proposal.json`, `baseline/`, `workspace/` |
| Proposal finalizer | Validates scope and emits unified diff. | `candidate.patch`, proposal status |
| Proposal judge | Prepares reruns, reads summaries, compares baseline vs candidate, writes decision. | `decision.json`, proposal status |

### Dependencies
| Depends On | For What |
| --- | --- |
| `scripts/eval_common.py` | Scenario loading, default path constants, JSON writing |
| `scripts/judge_evals.py` | Missing-field gating and batch summary generation |
| Python standard library | CLI parsing, filesystem copy/removal, JSON, diffs, glob-style matching |

## Scenario Preparation Flow
1. `prepare` resolves the scenario set from explicit names or `--all`.
2. The script derives a batch directory name from `--batch-name` or a UTC timestamp.
3. `prepare_batch()` refuses to reuse an existing batch directory unless `--force` is set; with `--force`, it removes the existing batch directory first.
4. For each scenario, the script confirms that `fixtures/<scenario.fixture>/` exists.
5. The fixture tree is copied into `<run-dir>/workspace/`.
6. Unless `--no-local-skills` is set, the script injects:
   - an eval-specific `AGENTS.md`
   - `.codex/support/` with copied repo support material
   - `.codex/skills/` with copied skill wrappers
7. The script writes:
   - `prompt.txt`
   - `result.json` with empty route fields, empty changed-paths list, empty notes, and the resolved workspace path
   - `scenario.snapshot.json`
   - `instructions.txt`
8. The script appends the run metadata to `batch.json`.

Observed repo context:

- Current fixtures are directory trees such as `fixtures/stack_known/`, `fixtures/scaffold_only/`, and `fixtures/playable_slice/`.
- Current scenario files use both `step-by-step` and `full-run` modes.
- Current scenario files also use optional fields such as `acceptable_first_routes`, `acceptable_next_recommendations`, and `expected_globs`.

### Support Bundle and Text Rewriting
When local skills are injected, the script copies support material from:

- `core/`
- `gamedev/`
- `productivity/`
- `templates/`
- `standards/`
- `docs/`

It then rewrites selected references inside text-like files so copied skill/support content points to `.codex/support/...` paths instead of the original repo-root paths. The rewrite applies to `.md`, `.txt`, `.json`, `.yaml`, `.yml`, and `SKILL.md`. Files that cannot be decoded as UTF-8 are skipped.

For proposal reruns, the same injection step accepts an `overlay_root`. Observed behavior: only support-bundle files and existing skill `SKILL.md` wrappers are overlaid from the proposal workspace into the prepared `.codex/` tree.

## Result Sync and Route Recording Flow

### Result Target Resolution
`sync-results` accepts:

- a single `result.json`
- a run directory that directly contains `result.json`
- a batch directory that contains `<run>/result.json`

`record-routes` accepts only one run directory or one `result.json`. If target resolution yields more than one result file, the command exits.

### Scenario Resolution
Both flows reconstruct the scenario by:

1. preferring `result.json["scenario_file"]` when it exists on disk
2. otherwise loading `<scenarios-root>/<scenario>.json`

### Sync Logic
`sync_result_file()`:

1. Loads the scenario and fixture directory.
2. Reads `result.json["workspace"]` and requires that the path exists.
3. Builds file maps for the fixture and workspace trees using `tracked_files()`.
4. Ignores paths matched by `RESULT_SYNC_IGNORE_PATTERNS`.
5. Writes the list of created or modified paths into `result.json["created_or_updated_paths"]`.

Observed behavior of changed-path detection:

- A new file in the workspace is recorded.
- A file whose bytes differ from the fixture copy is recorded.
- A deleted file is not recorded, because the comparison loop iterates workspace files, not fixture-only files.
- `.codex/**` is ignored, so injected support material does not pollute `created_or_updated_paths`.
- The ignore list includes both `.playwright/**` and `.playwrig/**` as written in the implementation.

### Route Recording Logic
`record-routes()`:

1. Loads exactly one result file.
2. Writes `actual_first_route` from `--first-route`.
3. Builds the set of expected next routes from `expected_next_recommendation` plus `acceptable_next_recommendations`.
4. If `--next-route` is provided, writes it.
5. If a next recommendation is expected but both `--next-route` and existing `actual_next_recommendation` are blank, exits with an error.
6. If `--note` is provided, replaces `result.json["notes"]`.

## Proposal Workflow

### Current Editable Set Surface
The current implementation exposes one editable set:

- `gamedev-phase3`

Observed editable patterns for this set:

- `docs/gamedev-workflow.md`
- `docs/gamedev-manual-runs.md`
- `docs/gamedev-autoimprovement.md`
- `gamedev/*/SKILL.md`
- `gamedev/templates/*.md`

### Proposal Preparation
`prepare-proposal()`:

1. Requires `<baseline-batch>/summary.json`.
2. Normalizes `focused_scenarios` and `full_scenarios` by resolving them through scenario files and deduplicating by canonical scenario name.
3. Defaults `full_scenarios` to every scenario under `evals/scenarios/` when `--full-scenarios` is omitted.
4. Requires every focused scenario to also be present in the full set.
5. Requires the baseline batch summary to contain every configured full scenario.
6. Creates `<proposal-dir>/baseline/` and `<proposal-dir>/workspace/` as sparse trees containing only files that match the editable patterns.
7. Writes `proposal.json` and `instructions.txt`.

Observed `proposal.json` fields include:

- proposal identity and timestamps
- editable set name and patterns
- baseline batch path
- focused/full scenario lists
- sparse baseline/workspace paths
- patch file path
- focused/full rerun batch paths
- status
- changed paths

### Proposal Finalization
`finalize-proposal()`:

1. Resolves `proposal.json` from a directory or direct file path.
2. Loads the sparse baseline root and editable workspace root from `proposal.json`.
3. Validates that every file present under `workspace/` matches the editable patterns.
4. Builds a unified diff between sparse baseline and sparse workspace.
5. Removes `<proposal-dir>/runs/` if it already exists.
6. Removes `<proposal-dir>/decision.json` if it already exists.
7. Updates `proposal.json` with `finalized_at_utc` and `changed_paths`.
8. If no changed paths exist:
   - deletes an existing patch file if present
   - marks the proposal `invalid`
   - writes `invalid_reason: "empty patch"`
   - exits with an error
9. Otherwise writes `candidate.patch`, marks the proposal `finalized`, and clears any prior `invalid_reason`.

Observed patch behavior:

- Added, removed, and changed files inside the sparse editable tree are all included in the patch.
- Patch generation reads files as UTF-8 text.

### Proposal Judging
`judge-proposal()`:

1. Requires `candidate.patch` to exist.
2. Requires the baseline batch `summary.json` to exist.
3. Prepares a focused rerun batch under `<proposal-dir>/runs/focused/` if it does not already exist.
4. Prepares rerun workspaces by copying the scenario fixture and then injecting `.codex/` support content using the proposal workspace as the overlay source.
5. Checks whether the focused batch already has enough route metadata to be judged.
6. If the focused batch is incomplete:
   - writes `decision.json` with status `awaiting_focused_runs`
   - prints instructions to complete manual runs
   - exits successfully
7. If the focused batch is ready:
   - ensures `summary.json` exists, calling `judge_evals.judge_batch()` when possible
   - compares the focused subset to the focused subset of the baseline summary
8. If the focused comparison regresses:
   - writes `decision.json` with status `regressed`
   - stops before preparing or judging the full batch
9. If focused and full scenario sets are identical:
   - reuses the focused comparison as the full result
   - writes a final decision without preparing a second batch
10. Otherwise:
   - prepares `<proposal-dir>/runs/full/` if needed
   - waits for that batch to become judgeable
   - compares the full candidate summary to the full baseline subset
   - writes the final decision

### Comparison Rules
Observed comparison precedence in `compare_summaries()`:

1. Fewer passed scenarios than baseline => `regressed`
2. Lower average score than baseline => `regressed`
3. Equal average score but more failed checks than baseline => `regressed`
4. More passed scenarios than baseline => `improved`
5. Higher average score than baseline => `improved`
6. Equal average score but fewer failed checks than baseline => `improved`
7. Otherwise => `flat`

Observed decision behavior:

- `judge-proposal()` never auto-applies `candidate.patch`.
- `awaiting_focused_runs` and `awaiting_full_runs` are non-error pending states.
- A final `regressed` result exits with status code `1`.
- Final `flat` and `improved` results exit with status code `0`.

## Key Constraints and Edge Cases
- `prepare` and `prepare-proposal` remove existing target directories only when `--force` is set.
- `inject_local_skill_bundle()` always removes an existing workspace `.codex/` directory before rebuilding it.
- When local skills are injected, the harness writes `workspace/AGENTS.md` unconditionally.
- `instructions.txt` always lists local skill/support extras as "Prepared extras", even when `prepare` ran with `--no-local-skills`.
- `overlay_skill_wrappers()` only updates wrappers for skills that were already discovered and copied from the repo. It does not create wrappers for new skill names that exist only in the overlay tree.
- Skill wrapper installation flattens skills by leaf directory name, so unique leaf names are assumed across discovered skill directories.
- `validate_editable_workspace()` rejects any out-of-scope file that exists in the proposal workspace, even if that file was added accidentally and is unrelated to the intended patch.
- `prepare_proposal_batch()` reuses an existing focused/full batch directory if it already exists.
- `ensure_batch_summary()` accepts an existing `summary.json` as-is and does not check whether it is stale relative to batch contents.
- `batch_ready_for_judge()` considers only route metadata completeness (`actual_first_route` and sometimes `actual_next_recommendation`), not file diff completeness.
- `record-routes` does not write `created_or_updated_paths`; that remains a separate sync step.

## What Remains Inferred or Unresolved
- The reason for the specific scoring weights in `judge_evals.py` is unresolved. The weights are observable, but no rationale is encoded in `run_evals.py`.
- The reason the only proposal editable set is `gamedev-phase3` is unresolved. The implementation proves the current restriction, not why this boundary was chosen.
- It is inferred that support-bundle path rewriting exists to make copied skills and docs self-contained inside prepared workspaces. The implementation proves the rewrite happens, but not the author’s intent.
- It is unresolved whether the `.playwrig/**` ignore pattern is intentional or a typo. The implementation only proves that the pattern is present.
- It is inferred that skill-leaf-name flattening was chosen for convenience of local `.codex/skills/` exposure. The implementation proves the flattening behavior, but not the design rationale.
