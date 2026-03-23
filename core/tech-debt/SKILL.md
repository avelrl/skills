---
name: tech-debt
description: "Track, categorize, and prioritize technical debt in a shared register."
argument-hint: "[scan|add|prioritize|report]"
user-invocable: true
---

Purpose: Keep one visible, practical register of technical debt and its urgency.

Use when:
- you need to scan for, record, prioritize, or summarize real technical debt
- the debt has maintenance, delivery, or reliability cost

Do not use for:
- cosmetic style nits
- feature backlog items with no ongoing engineering cost
- philosophical architecture debates with no actionable debt item

Inputs / Required Context:
- required: one mode from `scan|add|prioritize|report`
- read: relevant code, tests, docs, and the current debt register when it exists
- for `add`: description, affected area, acceptance reason, and practical impact

Outputs / Owned Artifacts:
- owns `docs/tech-debt-register.md`
- bootstraps the register if it does not exist
- updates the register only with high-signal items

Modes or Arguments:
- `scan`: inspect the codebase and add clearly actionable debt items
- `add`: record one explicit debt item
- `prioritize`: reorder or regroup the register by practical urgency
- `report`: summarize the current register

Execution Rules:
1. Ensure the canonical register exists before the first write.
2. Categorize debt as architecture, code quality, tests, documentation, dependencies, or performance.
3. For `scan`, look for high-signal indicators such as `TODO`, `FIXME`, duplication, risky untested logic, oversized code, or stale docs.
4. For `prioritize`, sort by impact, frequency, blast radius, and fix cost.
5. For `report`, summarize totals, oldest unresolved items, and debt that should move into the next cycle.

Failure / Stop Conditions:
- stop `add` if the item lacks a concrete description or affected area
- return an explicit empty-state summary if no meaningful debt is found
- do not add cosmetic noise to the register

Return Format:
- register path
- mode result summary
- highest-priority debt items or new entries
- next recommended cleanup target

Example Invocation:
- `/tech-debt scan`

Related Skills / Boundary:
- use `architecture-decision` when debt resolution requires a durable architectural choice
- do not turn this skill into a general project task tracker
