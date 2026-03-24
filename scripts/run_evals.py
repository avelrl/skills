#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, UTC
import difflib
from fnmatch import fnmatch
import json
from pathlib import Path
import shutil
import sys

from eval_common import (
    DEFAULT_FIXTURES_ROOT,
    DEFAULT_PROPOSALS_ROOT,
    DEFAULT_RUNS_ROOT,
    DEFAULT_SCENARIOS_ROOT,
    REPO_ROOT,
    Scenario,
    dump_json,
    load_scenario,
    load_scenarios,
)


SKILL_SOURCE_DIRS = ("core", "gamedev", "productivity")
SUPPORT_BUNDLE_DIRS = ("core", "gamedev", "productivity", "templates", "standards", "docs")
SKILL_TEXT_REWRITE_RULES = (
    ("docs/context-management.md", "__SUPPORT_DOC_CONTEXT__"),
    ("docs/gamedev-workflow.md", "__SUPPORT_DOC_WORKFLOW__"),
    ("docs/gamedev-manual-runs.md", "__SUPPORT_DOC_MANUAL_RUNS__"),
    ("docs/gamedev-autoimprovement.md", "__SUPPORT_DOC_AUTOIMPROVEMENT__"),
    ("gamedev/templates/", "__SUPPORT_GAMEDEV_TEMPLATES__"),
    ("gamedev/standards/", "__SUPPORT_GAMEDEV_STANDARDS__"),
    ("templates/", "__SUPPORT_SHARED_TEMPLATES__"),
    ("standards/", "__SUPPORT_SHARED_STANDARDS__"),
)
SKILL_TEXT_SUPPORT_TARGETS = {
    "__SUPPORT_DOC_CONTEXT__": "../../support/docs/context-management.md",
    "__SUPPORT_DOC_WORKFLOW__": "../../support/docs/gamedev-workflow.md",
    "__SUPPORT_DOC_MANUAL_RUNS__": "../../support/docs/gamedev-manual-runs.md",
    "__SUPPORT_DOC_AUTOIMPROVEMENT__": "../../support/docs/gamedev-autoimprovement.md",
    "__SUPPORT_GAMEDEV_TEMPLATES__": "../../support/gamedev/templates/",
    "__SUPPORT_GAMEDEV_STANDARDS__": "../../support/gamedev/standards/",
    "__SUPPORT_SHARED_TEMPLATES__": "../../support/templates/",
    "__SUPPORT_SHARED_STANDARDS__": "../../support/standards/",
}
SUPPORT_TEXT_SUPPORT_TARGETS = {
    "__SUPPORT_DOC_CONTEXT__": ".codex/support/docs/context-management.md",
    "__SUPPORT_DOC_WORKFLOW__": ".codex/support/docs/gamedev-workflow.md",
    "__SUPPORT_DOC_MANUAL_RUNS__": ".codex/support/docs/gamedev-manual-runs.md",
    "__SUPPORT_DOC_AUTOIMPROVEMENT__": ".codex/support/docs/gamedev-autoimprovement.md",
    "__SUPPORT_GAMEDEV_TEMPLATES__": ".codex/support/gamedev/templates/",
    "__SUPPORT_GAMEDEV_STANDARDS__": ".codex/support/gamedev/standards/",
    "__SUPPORT_SHARED_TEMPLATES__": ".codex/support/templates/",
    "__SUPPORT_SHARED_STANDARDS__": ".codex/support/standards/",
}
TEXT_REWRITE_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}
RESULT_SYNC_IGNORE_PATTERNS = (
    ".codex/**",
    ".git/**",
    ".DS_Store",
    "AGENTS.md",
    "coverage/**",
    "dist/**",
    "node_modules/**",
    "package-lock.json",
    "playwright-report/**",
    "progress.md",
    "test-results/**",
    ".playwright/**",
    ".playwrig/**",
)
PROPOSAL_EDITABLE_SETS = {
    "gamedev-phase3": (
        "docs/gamedev-workflow.md",
        "docs/gamedev-manual-runs.md",
        "docs/gamedev-autoimprovement.md",
        "gamedev/*/SKILL.md",
        "gamedev/templates/*.md",
    )
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare gamedev eval scenarios.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List available scenarios.")
    list_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)

    prepare_parser = subparsers.add_parser("prepare", help="Materialize one or more scenarios.")
    prepare_parser.add_argument("names", nargs="*", help="Scenario names. Omit with --all.")
    prepare_parser.add_argument("--all", action="store_true", help="Prepare every scenario.")
    prepare_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)
    prepare_parser.add_argument("--fixtures-root", type=Path, default=DEFAULT_FIXTURES_ROOT)
    prepare_parser.add_argument("--out-root", type=Path, default=DEFAULT_RUNS_ROOT)
    prepare_parser.add_argument("--batch-name", help="Optional batch directory name.")
    prepare_parser.add_argument("--force", action="store_true", help="Overwrite an existing batch directory.")
    prepare_parser.add_argument(
        "--no-local-skills",
        action="store_true",
        help="Prepare the bare fixture without copying the local skill bundle into the workspace.",
    )

    sync_parser = subparsers.add_parser(
        "sync-results",
        help="Refresh created_or_updated_paths in one run directory, one result.json, or a whole batch.",
    )
    sync_parser.add_argument("target", type=Path, help="Run directory, batch directory, or result.json path.")
    sync_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)
    sync_parser.add_argument("--fixtures-root", type=Path, default=DEFAULT_FIXTURES_ROOT)

    route_parser = subparsers.add_parser(
        "record-routes",
        help="Write actual_first_route and actual_next_recommendation into one result.json or one run directory.",
    )
    route_parser.add_argument("target", type=Path, help="Run directory or result.json path.")
    route_parser.add_argument("--first-route", required=True, help="Actual first route chosen during the run.")
    route_parser.add_argument(
        "--next-route",
        help="Actual next recommendation chosen during the run. Required when the scenario expects one and result.json is still blank.",
    )
    route_parser.add_argument(
        "--note",
        help="Optional note to write into result.json. Replaces the existing notes field when provided.",
    )
    route_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)

    proposal_parser = subparsers.add_parser(
        "prepare-proposal",
        help="Create an isolated phase-3 proposal workspace and metadata scaffold.",
    )
    proposal_parser.add_argument("--proposal-root", type=Path, default=DEFAULT_PROPOSALS_ROOT)
    proposal_parser.add_argument("--proposal-id", help="Optional proposal directory name.")
    proposal_parser.add_argument(
        "--editable-set",
        choices=sorted(PROPOSAL_EDITABLE_SETS),
        default="gamedev-phase3",
        help="Restricted editable file set for the proposal workspace.",
    )
    proposal_parser.add_argument(
        "--baseline-batch",
        type=Path,
        required=True,
        help="Batch directory with summary.json used as the comparison baseline.",
    )
    proposal_parser.add_argument(
        "--focused-scenarios",
        nargs="+",
        required=True,
        help="Scenario names for the cheap no-regression gate.",
    )
    proposal_parser.add_argument(
        "--full-scenarios",
        nargs="*",
        help="Optional explicit full-suite scenario list. Defaults to every scenario in evals/scenarios.",
    )
    proposal_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)
    proposal_parser.add_argument("--force", action="store_true", help="Overwrite an existing proposal directory.")

    finalize_parser = subparsers.add_parser(
        "finalize-proposal",
        help="Validate the isolated workspace and write candidate.patch plus metadata.",
    )
    finalize_parser.add_argument("target", type=Path, help="Proposal directory or proposal.json path.")

    judge_proposal_parser = subparsers.add_parser(
        "judge-proposal",
        help="Orchestrate focused/full rerun prep and compare proposal results to the baseline batch.",
    )
    judge_proposal_parser.add_argument("target", type=Path, help="Proposal directory or proposal.json path.")
    judge_proposal_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)
    judge_proposal_parser.add_argument("--fixtures-root", type=Path, default=DEFAULT_FIXTURES_ROOT)
    return parser


def scenario_dir_name(name: str) -> str:
    return name.replace(" ", "_")


def timestamp_slug() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def load_result(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def list_scenarios(scenarios_root: Path) -> int:
    scenarios = load_scenarios(scenarios_root)
    if not scenarios:
        print("No scenarios found.")
        return 1
    for scenario in scenarios:
        print(f"{scenario.name}: fixture={scenario.fixture} route={scenario.expected_first_route}")
        print(f"  prompt: {scenario.prompt}")
    return 0


def select_scenarios(args: argparse.Namespace) -> list[Scenario]:
    if args.all:
        return load_scenarios(args.scenarios_root)
    if not args.names:
        raise SystemExit("pass one or more scenario names or use --all")
    return [load_scenario(name, args.scenarios_root) for name in args.names]


def render_instructions(scenario: Scenario, workspace_dir: Path, result_path: Path) -> str:
    lines = [
        f"Scenario: {scenario.name}",
        f"Mode: {scenario.mode}",
        f"Prompt: {scenario.prompt}",
        "",
        "Manual flow:",
        "1. Open the prepared workspace.",
        "2. Run the agent against the prompt in prompt.txt.",
        "3. Fill result.json with the actual route fields and notes.",
        "   Required before judging: actual_first_route and actual_next_recommendation when the scenario expects a next step.",
        "   Optional helper: python scripts/run_evals.py sync-results <run-dir-or-batch-dir> to refresh created_or_updated_paths from the workspace diff.",
        "   Optional helper: python scripts/run_evals.py record-routes <run-dir> --first-route <skill> --next-route <skill> to write route metadata.",
        "4. Judge the run with scripts/judge_evals.py.",
        "",
        "Prepared extras:",
        "- scenario-local AGENTS.md is generated in the workspace root",
        "- local skill wrappers are exposed under .codex/skills/",
        "- shared repo references are copied into .codex/support/ as a snapshot",
        "- if a skill references root docs that are not present in the project tree, use the mirrored copies under .codex/support/docs/",
        "",
        f"Workspace: {workspace_dir}",
        f"Result file: {result_path}",
    ]
    return "\n".join(lines) + "\n"


def render_proposal_instructions(proposal_dir: Path, proposal: dict[str, object]) -> str:
    focused = ", ".join(str(name) for name in proposal["focused_scenarios"])
    full = ", ".join(str(name) for name in proposal["full_scenarios"])
    lines = [
        f"Proposal: {proposal['proposal_id']}",
        f"Editable set: {proposal['editable_set']}",
        f"Workspace: {proposal['workspace']}",
        f"Baseline batch: {proposal['baseline_batch']}",
        "",
        "Phase-3 flow:",
        "1. Edit only files inside workspace/.",
        "2. Run python scripts/run_evals.py finalize-proposal <proposal-dir>.",
        "3. Run python scripts/run_evals.py judge-proposal <proposal-dir>.",
        "4. If judge-proposal prepares rerun batches, execute those manual evals and rerun judge-proposal.",
        "5. Review decision.json and candidate.patch. Do not auto-apply the patch.",
        "",
        "Configured rerun gates:",
        f"- focused scenarios: {focused}",
        f"- full scenarios: {full}",
        "",
        "Safety rules:",
        "- only the restricted editable set may change",
        "- proposal reruns are prepared against the isolated workspace overlay, not the repo root",
        "- candidate runs under runs/ are disposable runtime artifacts",
    ]
    return "\n".join(lines) + "\n"


def discover_repo_skill_dirs() -> list[Path]:
    skill_dirs: list[Path] = []
    for root_name in SKILL_SOURCE_DIRS:
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        for skill_file in root.rglob("SKILL.md"):
            if "_archive" in skill_file.parts:
                continue
            skill_dirs.append(skill_file.parent)
    return sorted(skill_dirs)


def rewrite_paths(text: str, target_map: dict[str, str]) -> str:
    rewritten = text
    for source, placeholder in SKILL_TEXT_REWRITE_RULES:
        rewritten = rewritten.replace(source, placeholder)
    for placeholder, target in target_map.items():
        rewritten = rewritten.replace(placeholder, target)
    return rewritten


def rewrite_text_files(root: Path, target_map: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_REWRITE_SUFFIXES and path.name != "SKILL.md":
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rewritten = rewrite_paths(original, target_map)
        if rewritten != original:
            path.write_text(rewritten, encoding="utf-8")


def write_workspace_agents(workspace_dir: Path) -> None:
    content = """# Eval Workspace Guide

This directory is a prepared eval sandbox for one scenario.

## What Is In Scope

- project files in this workspace are the files under test
- local repo skills are available under `.codex/skills/`
- shared skill references are copied under `.codex/support/` as a local snapshot

## Working Rules

- treat `.codex/` as support material, not as the project to modify
- do not inspect sibling scenario directories or parent eval harness files unless explicitly asked
- do not depend on a global `$HOME/.codex`; use the local bundle in this workspace instead

## Support Paths

- shared repo docs, templates, and standards are mirrored under `.codex/support/`
- if a skill mentions root paths like `docs/context-management.md` or `docs/gamedev-workflow.md` and they do not exist in the project root, read the mirrored copies under `.codex/support/docs/`
"""
    (workspace_dir / "AGENTS.md").write_text(content, encoding="utf-8")


def overlay_support_bundle(target_root: Path, overlay_root: Path | None) -> None:
    if overlay_root is None or not overlay_root.exists():
        return

    for path in overlay_root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(overlay_root)
        if not relative_path.parts or relative_path.parts[0] not in SUPPORT_BUNDLE_DIRS:
            continue
        destination = target_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def install_support_bundle(workspace_dir: Path, overlay_root: Path | None = None) -> None:
    support_root = workspace_dir / ".codex" / "support"
    support_root.mkdir(parents=True, exist_ok=True)
    for directory_name in SUPPORT_BUNDLE_DIRS:
        shutil.copytree(REPO_ROOT / directory_name, support_root / directory_name)
    overlay_support_bundle(support_root, overlay_root)
    rewrite_text_files(support_root, SUPPORT_TEXT_SUPPORT_TARGETS)


def overlay_skill_wrappers(skills_root: Path, overlay_root: Path | None) -> None:
    if overlay_root is None or not overlay_root.exists():
        return

    for skill_file in overlay_root.rglob("SKILL.md"):
        relative_path = skill_file.relative_to(overlay_root)
        if len(relative_path.parts) < 3:
            continue
        if relative_path.parts[0] not in SKILL_SOURCE_DIRS:
            continue
        target_skill_file = skills_root / relative_path.parts[1] / "SKILL.md"
        if not target_skill_file.exists():
            continue
        target_skill_file.write_text(
            rewrite_paths(skill_file.read_text(encoding="utf-8"), SKILL_TEXT_SUPPORT_TARGETS),
            encoding="utf-8",
        )


def install_skill_wrappers(workspace_dir: Path, overlay_root: Path | None = None) -> None:
    skills_root = workspace_dir / ".codex" / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)

    for source_skill_dir in discover_repo_skill_dirs():
        target_skill_dir = skills_root / source_skill_dir.name
        shutil.copytree(source_skill_dir, target_skill_dir)

        skill_file = target_skill_dir / "SKILL.md"
        if skill_file.exists():
            skill_file.write_text(
                rewrite_paths(skill_file.read_text(encoding="utf-8"), SKILL_TEXT_SUPPORT_TARGETS),
                encoding="utf-8",
            )

    overlay_skill_wrappers(skills_root, overlay_root)


def inject_local_skill_bundle(workspace_dir: Path, overlay_root: Path | None = None) -> None:
    codex_dir = workspace_dir / ".codex"
    if codex_dir.exists():
        shutil.rmtree(codex_dir)
    write_workspace_agents(workspace_dir)
    install_support_bundle(workspace_dir, overlay_root)
    install_skill_wrappers(workspace_dir, overlay_root)


def should_ignore_result_sync_path(relative_path: str) -> bool:
    normalized = relative_path.strip().replace("\\", "/")
    if not normalized:
        return True
    return any(fnmatch(normalized, pattern) for pattern in RESULT_SYNC_IGNORE_PATTERNS)


def tracked_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root).as_posix()
        if should_ignore_result_sync_path(relative_path):
            continue
        files[relative_path] = path
    return files


def detect_created_or_updated_paths(fixture_dir: Path, workspace_dir: Path) -> list[str]:
    fixture_files = tracked_files(fixture_dir)
    workspace_files = tracked_files(workspace_dir)

    changed_paths: list[str] = []
    for relative_path, workspace_file in sorted(workspace_files.items()):
        fixture_file = fixture_files.get(relative_path)
        if fixture_file is None:
            changed_paths.append(relative_path)
            continue
        if workspace_file.read_bytes() != fixture_file.read_bytes():
            changed_paths.append(relative_path)
    return changed_paths


def scenario_from_result_payload(result: dict[str, object], scenarios_root: Path) -> Scenario:
    source = str(result.get("scenario_file", "")).strip()
    if source:
        source_path = Path(source)
        if source_path.exists():
            return Scenario.from_path(source_path)

    name = str(result.get("scenario", "")).strip()
    if not name:
        raise SystemExit("result file is missing scenario name")
    return load_scenario(name, scenarios_root)


def result_files_from_target(target: Path) -> list[Path]:
    if target.is_file():
        if target.name != "result.json":
            raise SystemExit(f"expected a result.json file, got: {target}")
        return [target]

    if not target.exists():
        raise SystemExit(f"target not found: {target}")

    direct_result = target / "result.json"
    if direct_result.exists():
        return [direct_result]

    result_files = sorted(target.glob("*/result.json"))
    if result_files:
        return result_files

    raise SystemExit(f"no result.json files found under {target}")


def sync_result_file(result_file: Path, scenarios_root: Path, fixtures_root: Path) -> None:
    result = load_result(result_file)
    scenario = scenario_from_result_payload(result, scenarios_root)
    fixture_dir = fixtures_root / scenario.fixture
    if not fixture_dir.exists():
        raise SystemExit(f"fixture not found for {scenario.name}: {fixture_dir}")

    workspace_value = str(result.get("workspace", "")).strip()
    if not workspace_value:
        raise SystemExit(f"{result_file}: workspace is missing from result.json")
    workspace_dir = Path(workspace_value)
    if not workspace_dir.exists():
        raise SystemExit(f"{result_file}: workspace not found: {workspace_dir}")

    changed_paths = detect_created_or_updated_paths(fixture_dir, workspace_dir)
    result["created_or_updated_paths"] = changed_paths
    dump_json(result_file, result)
    print(f"synced {scenario.name}: {len(changed_paths)} path(s)")


def sync_results(args: argparse.Namespace) -> int:
    result_files = result_files_from_target(args.target)
    for result_file in result_files:
        sync_result_file(result_file, args.scenarios_root, args.fixtures_root)
    return 0


def record_routes(args: argparse.Namespace) -> int:
    result_files = result_files_from_target(args.target)
    if len(result_files) != 1:
        raise SystemExit("record-routes expects one run directory or one result.json, not a whole batch")

    result_file = result_files[0]
    result = load_result(result_file)
    scenario = scenario_from_result_payload(result, args.scenarios_root)

    result["actual_first_route"] = args.first_route.strip()

    expected_next_routes = []
    if scenario.expected_next_recommendation:
        expected_next_routes.append(scenario.expected_next_recommendation)
    for candidate in scenario.acceptable_next_recommendations:
        if candidate and candidate not in expected_next_routes:
            expected_next_routes.append(candidate)

    existing_next = str(result.get("actual_next_recommendation", "")).strip()
    if args.next_route is not None:
        result["actual_next_recommendation"] = args.next_route.strip()
    elif expected_next_routes and not existing_next:
        raise SystemExit(
            f"{result_file}: --next-route is required because scenario {scenario.name} expects a next recommendation"
        )

    if args.note is not None:
        result["notes"] = args.note

    dump_json(result_file, result)
    actual_next = str(result.get("actual_next_recommendation", "")).strip()
    print(
        f"recorded {scenario.name}: first_route={result['actual_first_route']} "
        f"next_recommendation={actual_next or '<empty>'}"
    )
    return 0


def prepare_batch(
    scenarios: list[Scenario],
    batch_dir: Path,
    fixtures_root: Path,
    *,
    no_local_skills: bool,
    overlay_root: Path | None = None,
    force: bool = False,
) -> int:
    if batch_dir.exists():
        if not force:
            raise SystemExit(f"batch directory already exists: {batch_dir}")
        shutil.rmtree(batch_dir)
    batch_dir.mkdir(parents=True, exist_ok=True)

    batch_manifest: dict[str, object] = {
        "batch_name": batch_dir.name,
        "prepared_at_utc": datetime.now(UTC).isoformat(),
        "scenarios": [],
    }

    for scenario in scenarios:
        fixture_dir = fixtures_root / scenario.fixture
        if not fixture_dir.exists():
            raise SystemExit(f"fixture not found for {scenario.name}: {fixture_dir}")

        run_dir = batch_dir / scenario_dir_name(scenario.name)
        workspace_dir = run_dir / "workspace"
        shutil.copytree(fixture_dir, workspace_dir)
        if not no_local_skills:
            inject_local_skill_bundle(workspace_dir, overlay_root)

        prompt_path = run_dir / "prompt.txt"
        prompt_path.write_text(scenario.prompt + "\n", encoding="utf-8")

        result_path = run_dir / "result.json"
        dump_json(
            result_path,
            {
                "scenario": scenario.name,
                "scenario_file": str(scenario.source_path),
                "workspace": str(workspace_dir.resolve()),
                "prompt": scenario.prompt,
                "actual_first_route": "",
                "actual_next_recommendation": "",
                "created_or_updated_paths": [],
                "forbidden_triggered": [],
                "notes": "",
            },
        )

        dump_json(run_dir / "scenario.snapshot.json", scenario.to_jsonable())
        (run_dir / "instructions.txt").write_text(
            render_instructions(scenario, workspace_dir.resolve(), result_path.resolve()),
            encoding="utf-8",
        )

        batch_manifest["scenarios"].append(
            {
                "name": scenario.name,
                "fixture": scenario.fixture,
                "run_dir": str(run_dir.resolve()),
                "workspace": str(workspace_dir.resolve()),
                "result_file": str(result_path.resolve()),
            }
        )
        print(f"prepared {scenario.name}: {run_dir}")

    dump_json(batch_dir / "batch.json", batch_manifest)
    print(f"batch ready: {batch_dir}")
    return 0


def prepare_scenarios(args: argparse.Namespace) -> int:
    scenarios = select_scenarios(args)
    batch_name = args.batch_name or timestamp_slug()
    batch_dir = args.out_root / batch_name
    return prepare_batch(
        scenarios,
        batch_dir,
        args.fixtures_root,
        no_local_skills=args.no_local_skills,
        force=args.force,
    )


def proposal_file_from_target(target: Path) -> Path:
    if target.is_file():
        if target.name != "proposal.json":
            raise SystemExit(f"expected a proposal.json file, got: {target}")
        return target

    proposal_file = target / "proposal.json"
    if proposal_file.exists():
        return proposal_file
    raise SystemExit(f"proposal.json not found under {target}")


def load_proposal(proposal_file: Path) -> dict[str, object]:
    return json.loads(proposal_file.read_text(encoding="utf-8"))


def editable_patterns_for_set(name: str) -> tuple[str, ...]:
    try:
        return PROPOSAL_EDITABLE_SETS[name]
    except KeyError as exc:
        raise SystemExit(f"unknown editable set: {name}") from exc


def path_matches_patterns(relative_path: str, patterns: tuple[str, ...] | list[str]) -> bool:
    normalized = relative_path.strip().replace("\\", "/")
    return any(fnmatch(normalized, pattern) for pattern in patterns)


def copy_allowed_tree(source_root: Path, target_root: Path, patterns: tuple[str, ...] | list[str]) -> None:
    for path in source_root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(source_root).as_posix()
        if not path_matches_patterns(relative_path, patterns):
            continue
        destination = target_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)


def validate_editable_workspace(workspace_dir: Path, patterns: tuple[str, ...] | list[str]) -> None:
    for path in workspace_dir.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(workspace_dir).as_posix()
        if path_matches_patterns(relative_path, patterns):
            continue
        raise SystemExit(f"proposal workspace contains out-of-scope file: {relative_path}")


def all_files_under(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    if not root.exists():
        return files
    for path in root.rglob("*"):
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path
    return files


def unified_diff_text(before_path: Path | None, after_path: Path | None, relative_path: str) -> list[str]:
    before_lines = before_path.read_text(encoding="utf-8").splitlines(keepends=True) if before_path else []
    after_lines = after_path.read_text(encoding="utf-8").splitlines(keepends=True) if after_path else []
    from_file = f"a/{relative_path}" if before_path else "/dev/null"
    to_file = f"b/{relative_path}" if after_path else "/dev/null"
    return list(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=from_file,
            tofile=to_file,
        )
    )


def build_patch_artifact(baseline_dir: Path, workspace_dir: Path) -> tuple[str, list[str]]:
    baseline_files = all_files_under(baseline_dir)
    workspace_files = all_files_under(workspace_dir)
    changed_paths: list[str] = []
    patch_lines: list[str] = []

    for relative_path in sorted(set(baseline_files) | set(workspace_files)):
        before_path = baseline_files.get(relative_path)
        after_path = workspace_files.get(relative_path)
        if before_path and after_path and before_path.read_bytes() == after_path.read_bytes():
            continue
        changed_paths.append(relative_path)
        patch_lines.extend(unified_diff_text(before_path, after_path, relative_path))

    return "".join(patch_lines), changed_paths


def normalize_scenario_names(names: list[str], scenarios_root: Path) -> list[str]:
    normalized: list[str] = []
    for name in names:
        scenario = load_scenario(name, scenarios_root)
        if scenario.name not in normalized:
            normalized.append(scenario.name)
    return normalized


def prepare_proposal(args: argparse.Namespace) -> int:
    baseline_batch = args.baseline_batch.resolve()
    baseline_summary = baseline_batch / "summary.json"
    if not baseline_summary.exists():
        raise SystemExit(f"baseline summary not found: {baseline_summary}")
    baseline_summary_payload = load_summary(baseline_summary)

    editable_patterns = editable_patterns_for_set(args.editable_set)
    focused_scenarios = normalize_scenario_names(args.focused_scenarios, args.scenarios_root)
    if args.full_scenarios:
        full_scenarios = normalize_scenario_names(args.full_scenarios, args.scenarios_root)
    else:
        full_scenarios = [scenario.name for scenario in load_scenarios(args.scenarios_root)]

    missing_from_full = [name for name in focused_scenarios if name not in full_scenarios]
    if missing_from_full:
        missing = ", ".join(missing_from_full)
        raise SystemExit(f"full-scenarios must include every focused scenario: {missing}")

    baseline_scenarios = set(scenario_entries_by_name(baseline_summary_payload))
    missing_from_baseline = [name for name in full_scenarios if name not in baseline_scenarios]
    if missing_from_baseline:
        missing = ", ".join(missing_from_baseline)
        raise SystemExit(f"baseline batch summary is missing configured scenarios: {missing}")

    proposal_id = args.proposal_id or f"proposal-{timestamp_slug()}"
    proposal_dir = args.proposal_root / proposal_id
    if proposal_dir.exists():
        if not args.force:
            raise SystemExit(f"proposal directory already exists: {proposal_dir}")
        shutil.rmtree(proposal_dir)
    proposal_dir.mkdir(parents=True, exist_ok=True)

    baseline_dir = proposal_dir / "baseline"
    workspace_dir = proposal_dir / "workspace"
    copy_allowed_tree(REPO_ROOT, baseline_dir, editable_patterns)
    copy_allowed_tree(REPO_ROOT, workspace_dir, editable_patterns)

    proposal = {
        "proposal_id": proposal_id,
        "prepared_at_utc": datetime.now(UTC).isoformat(),
        "editable_set": args.editable_set,
        "editable_patterns": list(editable_patterns),
        "baseline_batch": str(baseline_batch),
        "focused_scenarios": focused_scenarios,
        "full_scenarios": full_scenarios,
        "baseline_editable_root": str(baseline_dir.resolve()),
        "workspace": str(workspace_dir.resolve()),
        "patch_file": str((proposal_dir / "candidate.patch").resolve()),
        "runs": {
            "focused": str((proposal_dir / "runs" / "focused").resolve()),
            "full": str((proposal_dir / "runs" / "full").resolve()),
        },
        "status": "prepared",
        "changed_paths": [],
    }
    proposal_file = proposal_dir / "proposal.json"
    dump_json(proposal_file, proposal)
    (proposal_dir / "instructions.txt").write_text(
        render_proposal_instructions(proposal_dir.resolve(), proposal),
        encoding="utf-8",
    )
    print(f"proposal ready: {proposal_dir}")
    print(f"edit here: {workspace_dir}")
    return 0


def finalize_proposal(args: argparse.Namespace) -> int:
    proposal_file = proposal_file_from_target(args.target)
    proposal = load_proposal(proposal_file)
    workspace_dir = Path(str(proposal["workspace"]))
    baseline_dir = Path(str(proposal["baseline_editable_root"]))
    patch_file = Path(str(proposal["patch_file"]))
    patterns = list(proposal["editable_patterns"])

    validate_editable_workspace(workspace_dir, patterns)
    patch_text, changed_paths = build_patch_artifact(baseline_dir, workspace_dir)

    runs_root = proposal_file.parent / "runs"
    if runs_root.exists():
        shutil.rmtree(runs_root)

    decision_file = proposal_file.parent / "decision.json"
    if decision_file.exists():
        decision_file.unlink()

    proposal["finalized_at_utc"] = datetime.now(UTC).isoformat()
    proposal["changed_paths"] = changed_paths

    if not changed_paths:
        if patch_file.exists():
            patch_file.unlink()
        proposal["status"] = "invalid"
        proposal["invalid_reason"] = "empty patch"
        dump_json(proposal_file, proposal)
        raise SystemExit("proposal is empty; edit workspace/ before finalizing")

    patch_file.write_text(patch_text, encoding="utf-8")
    proposal["status"] = "finalized"
    proposal.pop("invalid_reason", None)
    dump_json(proposal_file, proposal)
    print(f"finalized {proposal['proposal_id']}: {len(changed_paths)} changed path(s)")
    print(f"wrote: {patch_file}")
    return 0


def scenario_entries_by_name(summary: dict[str, object]) -> dict[str, dict[str, object]]:
    entries = summary.get("scenarios", [])
    if not isinstance(entries, list):
        raise SystemExit("summary.json is missing scenarios[]")

    mapping: dict[str, dict[str, object]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("scenario", "")).strip()
        if name:
            mapping[name] = entry
    return mapping


def subset_summary(summary: dict[str, object], scenario_names: list[str]) -> dict[str, object]:
    by_name = scenario_entries_by_name(summary)
    subset_entries: list[dict[str, object]] = []
    for name in scenario_names:
        entry = by_name.get(name)
        if entry is None:
            raise SystemExit(f"summary is missing scenario: {name}")
        subset_entries.append(entry)

    average_score = round(sum(float(entry.get("score", 0.0)) for entry in subset_entries) / len(subset_entries), 1)
    passed_count = sum(1 for entry in subset_entries if bool(entry.get("passed")))
    return {
        "scenario_count": len(subset_entries),
        "passed_count": passed_count,
        "failed_count": len(subset_entries) - passed_count,
        "average_score": average_score,
        "scenarios": subset_entries,
    }


def failed_checks_total(summary: dict[str, object]) -> int:
    total = 0
    for entry in summary.get("scenarios", []):
        if not isinstance(entry, dict):
            continue
        failed = entry.get("failed_checks", [])
        if isinstance(failed, list):
            total += len(failed)
    return total


def compare_summaries(label: str, baseline: dict[str, object], candidate: dict[str, object]) -> dict[str, object]:
    baseline_failed_checks = failed_checks_total(baseline)
    candidate_failed_checks = failed_checks_total(candidate)

    baseline_metrics = {
        "scenario_count": int(baseline["scenario_count"]),
        "passed_count": int(baseline["passed_count"]),
        "failed_count": int(baseline["failed_count"]),
        "average_score": float(baseline["average_score"]),
        "failed_checks_total": baseline_failed_checks,
    }
    candidate_metrics = {
        "scenario_count": int(candidate["scenario_count"]),
        "passed_count": int(candidate["passed_count"]),
        "failed_count": int(candidate["failed_count"]),
        "average_score": float(candidate["average_score"]),
        "failed_checks_total": candidate_failed_checks,
    }

    scenario_deltas: list[dict[str, object]] = []
    baseline_entries = scenario_entries_by_name(baseline)
    candidate_entries = scenario_entries_by_name(candidate)
    for name in sorted(candidate_entries):
        baseline_entry = baseline_entries[name]
        candidate_entry = candidate_entries[name]
        scenario_deltas.append(
            {
                "scenario": name,
                "baseline_score": baseline_entry.get("score"),
                "candidate_score": candidate_entry.get("score"),
                "baseline_passed": baseline_entry.get("passed"),
                "candidate_passed": candidate_entry.get("passed"),
                "baseline_failed_checks": baseline_entry.get("failed_checks", []),
                "candidate_failed_checks": candidate_entry.get("failed_checks", []),
            }
        )

    status = "flat"
    reason = "proposal matched the baseline metrics"
    if candidate_metrics["passed_count"] < baseline_metrics["passed_count"]:
        status = "regressed"
        reason = "fewer scenarios passed than baseline"
    elif candidate_metrics["average_score"] < baseline_metrics["average_score"]:
        status = "regressed"
        reason = "average score dropped below baseline"
    elif (
        candidate_metrics["average_score"] == baseline_metrics["average_score"]
        and candidate_metrics["failed_checks_total"] > baseline_metrics["failed_checks_total"]
    ):
        status = "regressed"
        reason = "failed check count increased at equal score"
    elif candidate_metrics["passed_count"] > baseline_metrics["passed_count"]:
        status = "improved"
        reason = "more scenarios passed than baseline"
    elif candidate_metrics["average_score"] > baseline_metrics["average_score"]:
        status = "improved"
        reason = "average score improved above baseline"
    elif (
        candidate_metrics["average_score"] == baseline_metrics["average_score"]
        and candidate_metrics["failed_checks_total"] < baseline_metrics["failed_checks_total"]
    ):
        status = "improved"
        reason = "failed check count decreased at equal score"

    return {
        "label": label,
        "status": status,
        "reason": reason,
        "baseline": baseline_metrics,
        "candidate": candidate_metrics,
        "scenario_deltas": scenario_deltas,
    }


def load_summary(summary_path: Path) -> dict[str, object]:
    return json.loads(summary_path.read_text(encoding="utf-8"))


def batch_ready_for_judge(batch_dir: Path, scenarios_root: Path) -> bool:
    from judge_evals import missing_result_fields

    result_files = sorted(batch_dir.glob("*/result.json"))
    if not result_files:
        return False

    for result_file in result_files:
        result = load_result(result_file)
        scenario = scenario_from_result_payload(result, scenarios_root)
        if missing_result_fields(scenario, result):
            return False
    return True


def ensure_batch_summary(batch_dir: Path, scenarios_root: Path) -> Path | None:
    from judge_evals import judge_batch

    summary_path = batch_dir / "summary.json"
    if summary_path.exists():
        return summary_path
    if not batch_dir.exists():
        return None
    if not batch_ready_for_judge(batch_dir, scenarios_root):
        return None

    judge_batch(batch_dir, scenarios_root)
    if summary_path.exists():
        return summary_path
    return None


def write_proposal_decision(proposal_file: Path, decision: dict[str, object]) -> None:
    proposal = load_proposal(proposal_file)
    proposal["status"] = decision["status"]
    proposal["decision_file"] = str((proposal_file.parent / "decision.json").resolve())
    proposal["last_judged_at_utc"] = decision["generated_at_utc"]
    dump_json(proposal_file, proposal)
    dump_json(proposal_file.parent / "decision.json", decision)


def prepare_proposal_batch(
    proposal: dict[str, object],
    batch_key: str,
    scenario_names: list[str],
    scenarios_root: Path,
    fixtures_root: Path,
) -> Path:
    batch_dir = Path(str(proposal["runs"][batch_key]))
    if batch_dir.exists():
        return batch_dir

    scenarios = [load_scenario(name, scenarios_root) for name in scenario_names]
    prepare_batch(
        scenarios,
        batch_dir,
        fixtures_root,
        no_local_skills=False,
        overlay_root=Path(str(proposal["workspace"])),
        force=False,
    )
    return batch_dir


def pending_decision(
    proposal: dict[str, object],
    status: str,
    next_action: str,
    *,
    focused: dict[str, object] | None = None,
) -> dict[str, object]:
    decision: dict[str, object] = {
        "proposal_id": proposal["proposal_id"],
        "status": status,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "patch_file": proposal["patch_file"],
        "baseline_batch": proposal["baseline_batch"],
        "changed_paths": proposal["changed_paths"],
        "next_action": next_action,
    }
    if focused is not None:
        decision["focused"] = focused
    return decision


def judge_proposal(args: argparse.Namespace) -> int:
    proposal_file = proposal_file_from_target(args.target)
    proposal = load_proposal(proposal_file)
    patch_file = Path(str(proposal["patch_file"]))
    if not patch_file.exists():
        raise SystemExit("proposal is not finalized; run finalize-proposal first")

    baseline_batch = Path(str(proposal["baseline_batch"]))
    baseline_summary_path = baseline_batch / "summary.json"
    if not baseline_summary_path.exists():
        raise SystemExit(f"baseline summary not found: {baseline_summary_path}")
    baseline_summary = load_summary(baseline_summary_path)

    focused_scenarios = [str(name) for name in proposal["focused_scenarios"]]
    full_scenarios = [str(name) for name in proposal["full_scenarios"]]

    focused_batch_dir = prepare_proposal_batch(
        proposal,
        "focused",
        focused_scenarios,
        args.scenarios_root,
        args.fixtures_root,
    )
    focused_summary_path = ensure_batch_summary(focused_batch_dir, args.scenarios_root)
    if focused_summary_path is None:
        decision = pending_decision(
            proposal,
            "awaiting_focused_runs",
            f"Complete manual runs under {focused_batch_dir} and rerun judge-proposal.",
        )
        write_proposal_decision(proposal_file, decision)
        print(f"focused rerun ready: {focused_batch_dir}")
        print("complete the focused runs, then rerun judge-proposal")
        return 0

    focused_candidate = subset_summary(load_summary(focused_summary_path), focused_scenarios)
    focused_baseline = subset_summary(baseline_summary, focused_scenarios)
    focused_comparison = compare_summaries("focused", focused_baseline, focused_candidate)

    if focused_comparison["status"] == "regressed":
        decision = pending_decision(
            proposal,
            "regressed",
            "Review candidate.patch and the focused rerun before preparing a full-suite batch.",
            focused=focused_comparison,
        )
        write_proposal_decision(proposal_file, decision)
        print("proposal regressed on focused scenarios")
        return 1

    if full_scenarios == focused_scenarios:
        final_status = str(focused_comparison["status"])
        next_action = (
            "Keep the patch for human review."
            if final_status == "improved"
            else "Patch is flat; keep only if the textual change itself is useful."
        )
        full_comparison = dict(focused_comparison)
        full_comparison["label"] = "full"
        decision = pending_decision(
            proposal,
            final_status,
            next_action,
            focused=focused_comparison,
        )
        decision["full"] = full_comparison
        write_proposal_decision(proposal_file, decision)
        print(f"proposal {final_status}: focused gate also served as full suite")
        return 0 if final_status in {"improved", "flat"} else 1

    full_batch_dir = prepare_proposal_batch(
        proposal,
        "full",
        full_scenarios,
        args.scenarios_root,
        args.fixtures_root,
    )
    full_summary_path = ensure_batch_summary(full_batch_dir, args.scenarios_root)
    if full_summary_path is None:
        decision = pending_decision(
            proposal,
            "awaiting_full_runs",
            f"Complete manual runs under {full_batch_dir} and rerun judge-proposal.",
            focused=focused_comparison,
        )
        write_proposal_decision(proposal_file, decision)
        print(f"full rerun ready: {full_batch_dir}")
        print("complete the full-suite runs, then rerun judge-proposal")
        return 0

    full_candidate = subset_summary(load_summary(full_summary_path), full_scenarios)
    full_baseline = subset_summary(baseline_summary, full_scenarios)
    full_comparison = compare_summaries("full", full_baseline, full_candidate)

    final_status = str(full_comparison["status"])
    next_action = "Keep the patch for human review; do not auto-apply." if final_status == "improved" else "Proposal did not beat the baseline; keep only as an inspection artifact."
    decision = pending_decision(
        proposal,
        final_status,
        next_action,
        focused=focused_comparison,
    )
    decision["full"] = full_comparison
    write_proposal_decision(proposal_file, decision)
    print(f"proposal {final_status}: {proposal['proposal_id']}")
    return 0 if final_status in {"improved", "flat"} else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "list":
        return list_scenarios(args.scenarios_root)
    if args.command == "prepare":
        return prepare_scenarios(args)
    if args.command == "sync-results":
        return sync_results(args)
    if args.command == "record-routes":
        return record_routes(args)
    if args.command == "prepare-proposal":
        return prepare_proposal(args)
    if args.command == "finalize-proposal":
        return finalize_proposal(args)
    if args.command == "judge-proposal":
        return judge_proposal(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
