---
name: gate-check
description: "Validate readiness to move from one game-project stage to the next."
argument-hint: "[systems-design|technical-setup|pre-production|production|polish|release]"
user-invocable: true
---

When this skill is invoked:

1. Determine the target phase:
   - use the explicit argument when provided,
   - otherwise infer the current phase with `project-stage-detect` heuristics and check the next stage.
2. Check only evidence that can be defended from the repository and project artifacts.
3. Use these artifacts as the primary sources:
   - `design/gdd/`
   - `docs/technical-preferences.md`
   - `docs/architecture/`
   - `prototypes/`
   - `production/`
   - `tests/`
   - `gamedev/templates/release-checklist.md` when release readiness is being assessed
4. Mark each check as:
   - PASS
   - CONCERN
   - FAIL
   - MANUAL CHECK NEEDED
5. Manual-only questions should cover things that code cannot prove, such as:
   - whether the core loop feels good,
   - whether recent playtests happened,
   - whether a release owner accepts known risks.
6. Output:
   - artifacts found,
   - blockers,
   - missing evidence,
   - verdict: PASS / CONCERNS / FAIL.
7. Only update `production/stage.txt` after a PASS verdict and explicit user confirmation.

Rules:

- Do not depend on removed workflows like `design-review`, `balance-check`, `playtest-report`, or `perf-profile`.
- If evidence is missing, say so directly instead of manufacturing a pass.
- This skill is stricter than `project-stage-detect`: it answers readiness, not just current state.
