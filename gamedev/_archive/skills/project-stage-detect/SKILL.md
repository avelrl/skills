---
name: project-stage-detect
description: "Assess a game project's current stage, gaps, and realistic next steps."
argument-hint: "[optional role filter]"
user-invocable: true
---

When this skill is invoked:

1. Scan the project for evidence across:
   - `design/`
   - `src/`
   - `docs/architecture/`
   - `production/`
   - `prototypes/`
   - `tests/`
2. Prefer observed facts over naming optimism:
   - count real files,
   - note incomplete or placeholder docs,
   - identify implemented systems that lack matching docs.
3. Determine the current stage:
   - Concept
   - Systems Design
   - Technical Setup
   - Pre-Production
   - Production
   - Polish
   - Release
4. Use `production/stage.txt` only as an explicit override when it exists.
5. Distinguish:
   - missing artifacts,
   - undocumented existing work,
   - likely stale or abandoned materials.
6. Ask targeted questions only for gaps that cannot be inferred from the repository.
7. Draft the output using `gamedev/templates/project-stage-report.md`.
8. Recommend only currently available follow-ups:
   - `architecture-decision`
   - `reverse-document`
   - `map-systems`
   - `design-system`
   - `prototype`
   - `setup-engine`
   - `gate-check`

Rules:

- Do not invent missing production process just because the donor toolkit expected it.
- If a subsystem exists in code but not in docs, call that out as a reverse-documentation candidate.
- If a role filter is provided, bias the recommendations; do not change the raw findings.
