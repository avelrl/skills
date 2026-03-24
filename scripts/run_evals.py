#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, UTC
from fnmatch import fnmatch
import json
from pathlib import Path
import shutil
import sys

from eval_common import (
    DEFAULT_FIXTURES_ROOT,
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


def install_support_bundle(workspace_dir: Path) -> None:
    support_root = workspace_dir / ".codex" / "support"
    support_root.mkdir(parents=True, exist_ok=True)
    for directory_name in SUPPORT_BUNDLE_DIRS:
        shutil.copytree(REPO_ROOT / directory_name, support_root / directory_name)
    rewrite_text_files(support_root, SUPPORT_TEXT_SUPPORT_TARGETS)


def install_skill_wrappers(workspace_dir: Path) -> None:
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


def inject_local_skill_bundle(workspace_dir: Path) -> None:
    codex_dir = workspace_dir / ".codex"
    if codex_dir.exists():
        shutil.rmtree(codex_dir)
    write_workspace_agents(workspace_dir)
    install_support_bundle(workspace_dir)
    install_skill_wrappers(workspace_dir)


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


def prepare_scenarios(args: argparse.Namespace) -> int:
    scenarios = select_scenarios(args)
    batch_name = args.batch_name or timestamp_slug()
    batch_dir = args.out_root / batch_name
    if batch_dir.exists():
        if not args.force:
            raise SystemExit(f"batch directory already exists: {batch_dir}")
        shutil.rmtree(batch_dir)
    batch_dir.mkdir(parents=True, exist_ok=True)

    batch_manifest: dict[str, object] = {
        "batch_name": batch_name,
        "prepared_at_utc": datetime.now(UTC).isoformat(),
        "scenarios": [],
    }

    for scenario in scenarios:
        fixture_dir = args.fixtures_root / scenario.fixture
        if not fixture_dir.exists():
            raise SystemExit(f"fixture not found for {scenario.name}: {fixture_dir}")

        run_dir = batch_dir / scenario_dir_name(scenario.name)
        workspace_dir = run_dir / "workspace"
        shutil.copytree(fixture_dir, workspace_dir)
        if not args.no_local_skills:
            inject_local_skill_bundle(workspace_dir)

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
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
