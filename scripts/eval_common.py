#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIOS_ROOT = REPO_ROOT / "evals" / "scenarios"
DEFAULT_FIXTURES_ROOT = REPO_ROOT / "fixtures"
DEFAULT_RUNS_ROOT = REPO_ROOT / "reports" / "evals" / "runs"
DEFAULT_PROPOSALS_ROOT = REPO_ROOT / "reports" / "evals" / "proposals"


@dataclass(frozen=True)
class Scenario:
    name: str
    fixture: str
    mode: str
    prompt: str
    expected_first_route: str | None
    acceptable_first_routes: list[str]
    expected_next_recommendation: str | None
    acceptable_next_recommendations: list[str]
    expected_paths: list[str]
    expected_globs: list[str]
    forbidden_behaviors: list[str]
    source_path: Path

    @classmethod
    def from_path(cls, path: Path) -> "Scenario":
        payload = json.loads(path.read_text(encoding="utf-8"))
        required = ["name", "fixture", "mode", "prompt"]
        missing = [key for key in required if key not in payload or payload[key] == ""]
        if missing:
            raise ValueError(f"{path}: missing required fields: {', '.join(missing)}")
        expected_first_route = payload.get("expected_first_route")
        acceptable_first_routes = list(payload.get("acceptable_first_routes", []))
        if expected_first_route in ("", None):
            expected_first_route = None
        if not expected_first_route and not acceptable_first_routes:
            raise ValueError(f"{path}: missing required route expectation")
        return cls(
            name=payload["name"],
            fixture=payload["fixture"],
            mode=payload["mode"],
            prompt=payload["prompt"],
            expected_first_route=expected_first_route,
            acceptable_first_routes=acceptable_first_routes,
            expected_next_recommendation=payload.get("expected_next_recommendation"),
            acceptable_next_recommendations=list(
                payload.get("acceptable_next_recommendations", [])
            ),
            expected_paths=list(payload.get("expected_paths", [])),
            expected_globs=list(payload.get("expected_globs", [])),
            forbidden_behaviors=list(payload.get("forbidden_behaviors", [])),
            source_path=path,
        )

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "fixture": self.fixture,
            "mode": self.mode,
            "prompt": self.prompt,
            "expected_first_route": self.expected_first_route,
            "acceptable_first_routes": self.acceptable_first_routes,
            "expected_next_recommendation": self.expected_next_recommendation,
            "acceptable_next_recommendations": self.acceptable_next_recommendations,
            "expected_paths": self.expected_paths,
            "expected_globs": self.expected_globs,
            "forbidden_behaviors": self.forbidden_behaviors,
            "source_path": str(self.source_path),
        }


def load_scenarios(root: Path = DEFAULT_SCENARIOS_ROOT) -> list[Scenario]:
    return [Scenario.from_path(path) for path in sorted(root.glob("*.json"))]


def load_scenario(name: str, root: Path = DEFAULT_SCENARIOS_ROOT) -> Scenario:
    path = root / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"scenario not found: {path}")
    return Scenario.from_path(path)


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
