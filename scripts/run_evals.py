#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, UTC
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
