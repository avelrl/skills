---
name: prototype
description: "Build a throwaway game prototype to answer one concrete design or technical question."
argument-hint: "<question-or-mechanic>"
user-invocable: true
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
- optional: `docs/technical-preferences.md`, `design/gdd/systems-index.md`, relevant design docs in `design/gdd/`, and `standards/prototype-code.md`

Outputs / Owned Artifacts:
- owns `prototypes/[slug]/`
- owns `prototypes/[slug]/REPORT.md`
- uses `gamedev/templates/prototype-report.md`
- may include a lightweight proof artifact such as a screenshot or short capture when cheap and useful
- keeps prototype code isolated from production code

Modes or Arguments:
- `<question-or-mechanic>`: normalized into one testable hypothesis

Execution Rules:
1. Turn the prompt into one explicit hypothesis.
2. Read only the project context needed to make the prototype credible.
3. If possible, identify the related system in `design/gdd/systems-index.md` or a likely affected design doc.
4. Define the smallest prototype that can answer the question.
5. Implement only the code needed to test the hypothesis; hardcoded values and placeholder assets are acceptable.
6. Run the prototype, capture observations, and write `REPORT.md` using the canonical prototype-report template.
7. The report contract is fixed: hypothesis, run notes, approach, result, observations or metrics, recommendation.
8. `REPORT.md` must also include:
   - `Affected Design Docs`
   - `Suggested Baseline Values`
   - `Deferred Tuning Questions`
   - `Recommended Follow-Up`
   - `Next Documentation Action`
   - `Evidence Artifacts`
9. `Suggested Baseline Values` should contain concrete defaults only when the prototype yields actionable values; otherwise explicitly record `None recommended`.
10. `Recommended Follow-Up` must explicitly choose one of:
   - update existing design doc
   - create new design doc
   - no design change needed
11. When the target doc or system is known, name it directly in `Recommended Follow-Up` and `Next Documentation Action`.
12. If visual proof is cheap and useful, save one screenshot or equivalent lightweight artifact in the prototype folder and list it in `Evidence Artifacts`.
13. Do not promote prototype code into production through gradual cleanup.

Failure / Stop Conditions:
- stop if the question is too vague to test
- stop if the request actually requires production-grade integration instead of a disposable spike

Return Format:
- prototype path
- report path
- hypothesis
- result
- observations or metrics
- affected design docs
- suggested baseline values
- recommendation: `PROCEED`, `PIVOT`, or `KILL`
- next documentation action
- evidence artifacts, if any

Example Invocation:
- `/prototype can-players-read-enemy-telegraphs-at-60fps`

Related Skills / Boundary:
- use `design-system` before or after the prototype to keep design docs aligned with the learning
- use `architecture-decision` only if the prototype forces a durable technical choice
