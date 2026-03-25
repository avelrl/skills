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
- optional: `docs/technical-preferences.md`, `design/gdd/systems-index.md`, relevant design docs in `design/gdd/`, existing related `prototypes/*/REPORT.md`, and `standards/prototype-code.md`

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
2. Check whether an existing prototype report already answers the same question well enough to choose a default.
3. If the question is already effectively closed by existing evidence, do not create a near-duplicate spike; route to `design-system` or `implement-system` instead.
4. Read only the project context needed to make the prototype credible.
5. If possible, identify the related system in `design/gdd/systems-index.md` or a likely affected design doc.
6. Define the smallest prototype that can answer the question.
7. Implement only the code needed to test the hypothesis; hardcoded values and placeholder assets are acceptable.
8. Run the prototype, capture observations, and write `REPORT.md` using the canonical prototype-report template.
9. The report contract is fixed: hypothesis, run notes, approach, result, observations or metrics, recommendation.
10. `REPORT.md` must also include:
   - `Affected Design Docs`
   - `Suggested Baseline Values`
   - `Deferred Tuning Questions`
   - `Recommended Follow-Up`
   - `Next Documentation Action`
   - `Evidence Artifacts`
11. `Suggested Baseline Values` should contain concrete defaults only when the prototype yields actionable values; otherwise explicitly record `None recommended`.
12. `Recommended Follow-Up` must explicitly choose one of:
   - update existing design doc
   - create new design doc
   - no design change needed
13. When the target doc or system is known, name it directly in `Recommended Follow-Up` and `Next Documentation Action`.
14. If visual proof is cheap and useful, save one screenshot or equivalent lightweight artifact in the prototype folder and list it in `Evidence Artifacts`.
15. When a target design doc already exists and the prototype result is actionable, update that doc or its evidence section in the same pass unless the user explicitly asked for the spike only.
16. Do not promote prototype code into production through gradual cleanup.

Failure / Stop Conditions:
- stop if the question is too vague to test
- stop if the request actually requires production-grade integration instead of a disposable spike
- stop if an existing accepted prototype already answers the same question and implementation or playtest evidence has not contradicted it

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
- use `implement-system` only after prototype findings are folded back into the canonical design docs
- use `architecture-decision` only if the prototype forces a durable technical choice
