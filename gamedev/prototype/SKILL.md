---
name: prototype
description: "Build a throwaway game prototype to answer one concrete design or technical question."
argument-hint: "<question-or-mechanic>"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

Purpose: Build a disposable prototype that answers one concrete design or technical question.

Use when:
- a mechanic, feel question, or technical risk is still uncertain
- the team needs evidence before expanding a system design

Do not use for:
- production implementation
- backlog-driven feature completion
- polishing code that should remain disposable

Inputs / Required Context:
- required: one explicit prototype question or mechanic
- optional: `docs/technical-preferences.md` and relevant design docs in `design/gdd/`

Outputs / Owned Artifacts:
- owns `prototypes/[slug]/`
- owns `prototypes/[slug]/REPORT.md`
- keeps prototype code isolated from production code

Modes or Arguments:
- `<question-or-mechanic>`: normalized into one testable hypothesis

Execution Rules:
1. Turn the prompt into one explicit hypothesis.
2. Read only the project context needed to make the prototype credible.
3. Define the smallest prototype that can answer the question.
4. Implement only the code needed to test the hypothesis; hardcoded values and placeholder assets are acceptable.
5. Run the prototype, capture observations, and write `REPORT.md`.
6. The report contract is fixed: hypothesis, approach, result, observations or metrics, recommendation.

Failure / Stop Conditions:
- stop if the question is too vague to test
- stop if the request actually requires production-grade integration instead of a disposable spike
- do not promote prototype code into production through gradual cleanup

Return Format:
- prototype path
- report path
- hypothesis
- result
- observations or metrics
- recommendation: `PROCEED`, `PIVOT`, or `KILL`

Example Invocation:
- `/prototype can-players-read-enemy-telegraphs-at-60fps`

Related Skills / Boundary:
- use `design-system` before or after the prototype to keep design docs aligned with the learning
- use `architecture-decision` only if the prototype forces a durable technical choice
