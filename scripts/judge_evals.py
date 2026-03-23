#!/usr/bin/env python3
from __future__ import annotations

import argparse
from fnmatch import fnmatch
import json
from pathlib import Path
import sys

from eval_common import DEFAULT_SCENARIOS_ROOT, Scenario, dump_json, load_scenario


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Judge prepared gamedev eval runs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    judge_parser = subparsers.add_parser("judge", help="Judge a single result.json file.")
    judge_parser.add_argument("result_file", type=Path)
    judge_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)

    batch_parser = subparsers.add_parser("judge-batch", help="Judge every result.json under a batch directory.")
    batch_parser.add_argument("batch_dir", type=Path)
    batch_parser.add_argument("--scenarios-root", type=Path, default=DEFAULT_SCENARIOS_ROOT)
    return parser


def load_result(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_paths(result: dict[str, object]) -> set[str]:
    values = result.get("created_or_updated_paths", [])
    if not isinstance(values, list):
        return set()
    return {str(value).strip() for value in values if str(value).strip()}


def path_exists(workspace: Path | None, relative_path: str, recorded_paths: set[str]) -> bool:
    if relative_path in recorded_paths:
        return True
    if workspace is None:
        return False
    return (workspace / relative_path).exists()


def glob_exists(workspace: Path | None, pattern: str, recorded_paths: set[str]) -> bool:
    if any(fnmatch(candidate, pattern) for candidate in recorded_paths):
        return True
    if workspace is None:
        return False
    return any(workspace.glob(pattern))


def score_run(scenario: Scenario, result: dict[str, object]) -> dict[str, object]:
    workspace_value = str(result.get("workspace", "")).strip()
    workspace = Path(workspace_value) if workspace_value else None
    if workspace is not None and not workspace.exists():
        workspace = None

    recorded_paths = candidate_paths(result)
    actual_first_route = str(result.get("actual_first_route", "")).strip()
    actual_next = str(result.get("actual_next_recommendation", "")).strip()
    forbidden_triggered = result.get("forbidden_triggered", [])
    if not isinstance(forbidden_triggered, list):
        forbidden_triggered = [str(forbidden_triggered)]

    checks: list[dict[str, object]] = []
    points_total = 0.0
    points_earned = 0.0

    route_ok = actual_first_route == scenario.expected_first_route
    checks.append(
        {
            "name": "first_route",
            "passed": route_ok,
            "expected": scenario.expected_first_route,
            "actual": actual_first_route,
            "weight": 40,
        }
    )
    points_total += 40
    points_earned += 40 if route_ok else 0

    if scenario.expected_next_recommendation:
        next_ok = actual_next == scenario.expected_next_recommendation
        checks.append(
            {
                "name": "next_recommendation",
                "passed": next_ok,
                "expected": scenario.expected_next_recommendation,
                "actual": actual_next,
                "weight": 10,
            }
        )
        points_total += 10
        points_earned += 10 if next_ok else 0

    expected_items = scenario.expected_paths + scenario.expected_globs
    per_item_weight = 30 / len(expected_items) if expected_items else 0
    for relative_path in scenario.expected_paths:
        passed = path_exists(workspace, relative_path, recorded_paths)
        checks.append(
            {
                "name": f"path:{relative_path}",
                "passed": passed,
                "expected": relative_path,
                "actual": "exists" if passed else "missing",
                "weight": per_item_weight,
            }
        )
        points_total += per_item_weight
        points_earned += per_item_weight if passed else 0

    for pattern in scenario.expected_globs:
        passed = glob_exists(workspace, pattern, recorded_paths)
        checks.append(
            {
                "name": f"glob:{pattern}",
                "passed": passed,
                "expected": pattern,
                "actual": "matched" if passed else "missing",
                "weight": per_item_weight,
            }
        )
        points_total += per_item_weight
        points_earned += per_item_weight if passed else 0

    forbidden_ok = len(forbidden_triggered) == 0
    checks.append(
        {
            "name": "forbidden_behaviors",
            "passed": forbidden_ok,
            "expected": [],
            "actual": forbidden_triggered,
            "weight": 20,
        }
    )
    points_total += 20
    points_earned += 20 if forbidden_ok else 0

    failed_checks = [check["name"] for check in checks if not check["passed"]]
    score = round((points_earned / points_total) * 100, 1) if points_total else 0.0
    passed = len(failed_checks) == 0
    return {
        "scenario": scenario.name,
        "score": score,
        "passed": passed,
        "failed_checks": failed_checks,
        "checks": checks,
        "notes": result.get("notes", ""),
        "workspace": workspace_value,
    }


def scenario_from_result(result: dict[str, object], scenarios_root: Path) -> Scenario:
    source = str(result.get("scenario_file", "")).strip()
    if source:
        path = Path(source)
        if path.exists():
            return Scenario.from_path(path)
    name = str(result.get("scenario", "")).strip()
    if not name:
        raise SystemExit("result file is missing scenario name")
    return load_scenario(name, scenarios_root)


def judge_result(result_file: Path, scenarios_root: Path) -> dict[str, object]:
    result = load_result(result_file)
    scenario = scenario_from_result(result, scenarios_root)
    summary = score_run(scenario, result)
    summary_path = result_file.with_name("judgement.json")
    dump_json(summary_path, summary)
    print(f"{summary['scenario']}: score={summary['score']} passed={summary['passed']}")
    if summary["failed_checks"]:
        print("  failed:", ", ".join(summary["failed_checks"]))
    print(f"  wrote: {summary_path}")
    return summary


def judge_batch(batch_dir: Path, scenarios_root: Path) -> int:
    result_files = sorted(batch_dir.glob("*/result.json"))
    if not result_files:
        raise SystemExit(f"no result.json files found under {batch_dir}")

    summaries = [judge_result(result_file, scenarios_root) for result_file in result_files]
    passed = sum(1 for summary in summaries if summary["passed"])
    average_score = round(sum(float(summary["score"]) for summary in summaries) / len(summaries), 1)
    batch_summary = {
        "batch_dir": str(batch_dir.resolve()),
        "scenario_count": len(summaries),
        "passed_count": passed,
        "failed_count": len(summaries) - passed,
        "average_score": average_score,
        "scenarios": summaries,
    }
    summary_path = batch_dir / "summary.json"
    dump_json(summary_path, batch_summary)
    print(f"batch summary: average_score={average_score} passed={passed}/{len(summaries)}")
    print(f"wrote: {summary_path}")
    return 0 if passed == len(summaries) else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "judge":
        judge_result(args.result_file, args.scenarios_root)
        return 0
    if args.command == "judge-batch":
        return judge_batch(args.batch_dir, args.scenarios_root)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
