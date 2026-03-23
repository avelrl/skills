#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, UTC
import os
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
SOURCE_BUNDLE_DIRS = ("core", "gamedev", "productivity", "templates", "standards")
DOC_SOURCE_FILES = ("context-management.md", "gamedev-workflow.md", "gamedev-manual-runs.md", "gamedev-autoimprovement.md")


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
    return parser


def scenario_dir_name(name: str) -> str:
    return name.replace(" ", "_")


def timestamp_slug() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


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
        "3. Fill result.json with the actual route and notes.",
        "4. Judge the run with scripts/judge_evals.py.",
        "",
        "Prepared extras:",
        "- local AGENTS.md is copied into the workspace",
        "- local docs/ workflow references are copied into the workspace",
        "- local skills are exposed under .codex/skills/",
        "",
        f"Workspace: {workspace_dir}",
        f"Result file: {result_path}",
    ]
    return "\n".join(lines) + "\n"


def copytree_merge(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True)


def discover_skill_dirs(workspace_dir: Path) -> list[Path]:
    skill_dirs: list[Path] = []
    for root_name in SKILL_SOURCE_DIRS:
        root = workspace_dir / root_name
        if not root.exists():
            continue
        for skill_file in root.rglob("SKILL.md"):
            if "_archive" in skill_file.parts:
                continue
            skill_dirs.append(skill_file.parent)
    return sorted(skill_dirs)


def create_skill_symlink(link_path: Path, target_dir: Path) -> None:
    if link_path.exists() or link_path.is_symlink():
        if link_path.is_dir() and not link_path.is_symlink():
            shutil.rmtree(link_path)
        else:
            link_path.unlink()
    relative_target = os.path.relpath(target_dir, start=link_path.parent)
    os.symlink(relative_target, link_path)


def inject_local_skill_bundle(workspace_dir: Path) -> None:
    for directory_name in SOURCE_BUNDLE_DIRS:
        copytree_merge(REPO_ROOT / directory_name, workspace_dir / directory_name)

    docs_dir = workspace_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    repo_docs = REPO_ROOT / "docs"
    for filename in DOC_SOURCE_FILES:
        src = repo_docs / filename
        if src.exists():
            shutil.copy2(src, docs_dir / filename)

    shutil.copy2(REPO_ROOT / "AGENTS.md", workspace_dir / "AGENTS.md")

    codex_skills_dir = workspace_dir / ".codex" / "skills"
    codex_skills_dir.mkdir(parents=True, exist_ok=True)
    for skill_dir in discover_skill_dirs(workspace_dir):
        link_path = codex_skills_dir / skill_dir.name
        create_skill_symlink(link_path, skill_dir)


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
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
