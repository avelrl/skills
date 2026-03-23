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


@dataclass(frozen=True)
class Scenario:
    name: str
    fixture: str
    mode: str
    prompt: str
    expected_first_route: str
    expected_next_recommendation: str | None
    expected_paths: list[str]
    expected_globs: list[str]
    forbidden_behaviors: list[str]
    source_path: Path

    @classmethod
    def from_path(cls, path: Path) -> "Scenario":
        payload = json.loads(path.read_text(encoding="utf-8"))
        required = ["name", "fixture", "mode", "prompt", "expected_first_route"]
        missing = [key for key in required if key not in payload or payload[key] == ""]
        if missing:
            raise ValueError(f"{path}: missing required fields: {', '.join(missing)}")
        return cls(
            name=payload["name"],
            fixture=payload["fixture"],
            mode=payload["mode"],
            prompt=payload["prompt"],
            expected_first_route=payload["expected_first_route"],
            expected_next_recommendation=payload.get("expected_next_recommendation"),
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
            "expected_next_recommendation": self.expected_next_recommendation,
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
