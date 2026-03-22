---
name: asset-audit
description: "Audit game assets against naming, size, format, and reference integrity rules."
argument-hint: "[category|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

Purpose: Audit game assets for convention drift, reference integrity, and obvious budget problems.

Use when:
- a project needs a quick asset health check by category or across the whole tree
- you need evidence before cleanup or pipeline fixes

Do not use for:
- generating assets
- deleting or renaming files without confirmation
- localization table validation

Inputs / Required Context:
- required: one category or `all`
- read project rules first from `docs/technical-preferences.md` when available
- fall back to `gamedev/standards/data-files.md` and any relevant art or audio bible already present

Outputs / Owned Artifacts:
- no file output by default
- returns an inline audit report using `Summary -> Findings -> Risks -> Recommended Next Step`

Modes or Arguments:
- `[category]`: audit one asset class
- `all`: audit standard asset directories together

Execution Rules:
1. Resolve the requested asset scope and load project conventions or fallback assumptions.
2. Check naming, format, size or dimension budgets, broken references, orphaned assets, and missing expected assets.
3. Group findings as violations, missing references, orphans, and missing expected assets.
4. If nothing is wrong, return an explicit zero-findings summary instead of a silent success.

Failure / Stop Conditions:
- stop if the requested category cannot be mapped to a real project area
- stop if no relevant asset directories exist
- never assume `unused` means safe to delete; report it as orphaned unless confirmed otherwise

Return Format:
- `Summary`
- `Findings`
- `Risks`
- `Recommended Next Step`

Example Invocation:
- `/asset-audit textures`

Related Skills / Boundary:
- use `localize` for string tables and locale coverage
- do not turn this skill into an automatic cleanup workflow
