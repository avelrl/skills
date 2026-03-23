---
paths:
  - "design/gdd/**"
---

# Design Document Rules

- A system design doc should remove implementation ambiguity, not narrate the whole project.
- Core sections for active system docs:
  - overview
  - scope boundaries
  - player experience goal
  - core rules
  - interactions
  - evidence or prototype inputs
  - assumptions
  - formulas or data rules
  - edge cases
  - dependencies
  - acceptance criteria
  - open questions
- Scope should be split into `In MVP`, `In Vertical Slice`, and `Deferred / Later`.
- Evidence sections should reference concrete prototype reports when they exist and say `None yet` when they do not.
- For `design/gdd/systems-index.md`, use the canonical system statuses:
  - `identified`
  - `designed`
  - `prototyped`
  - `informed-by-prototype`
  - `implemented`
  - `integrated`
- Do not downgrade an existing system status during an index refresh unless the previous status was clearly wrong.
- Add tuning knobs when balance matters; do not invent them for systems that do not need tuning.
- Every rule should be testable or observable. Replace vague words like "fun" or "feels good" with concrete behavior.
- Document unresolved decisions explicitly instead of hiding them in prose.
- When prototype evidence changes scope or defaults, rewrite the canonical doc sections so they stay internally consistent.
- Update docs when implementation meaningfully changes; stale design docs are worse than missing ones.
