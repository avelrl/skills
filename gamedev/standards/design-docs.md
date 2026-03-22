---
paths:
  - "design/gdd/**"
---

# Design Document Rules

- A system design doc should remove implementation ambiguity, not narrate the whole project.
- Core sections for active system docs:
  - overview
  - player experience goal
  - core rules
  - interactions
  - formulas or data rules
  - edge cases
  - dependencies
  - acceptance criteria
  - open questions
- Add tuning knobs when balance matters; do not invent them for systems that do not need tuning.
- Every rule should be testable or observable. Replace vague words like "fun" or "feels good" with concrete behavior.
- Document unresolved decisions explicitly instead of hiding them in prose.
- Update docs when implementation meaningfully changes; stale design docs are worse than missing ones.
