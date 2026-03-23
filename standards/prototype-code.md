---
paths:
  - "prototypes/**"
---

# Prototype Code Standards (Relaxed)

Prototypes are throwaway code for validating ideas. Standards are intentionally
relaxed to maximize iteration speed. The goal is learning, not production quality.

## What's Allowed in Prototypes
- Hardcoded values (no need for data-driven config)
- Minimal or no doc comments
- Simple architecture (no dependency injection required)
- Singletons and global state
- Copy-pasted code (no need for abstraction)
- Debug output left in place
- Placeholder art and audio
- Quick-and-dirty solutions

## What's Still Required
- Each prototype lives in its own subdirectory: `prototypes/[name]/`
- Every prototype MUST have a `REPORT.md` that captures:
  - What hypothesis is being tested
  - How to run or evaluate the prototype
  - Current state or outcome
  - Findings, observations, or metrics
  - Affected design docs and recommended follow-up
- A short `README.md` is optional only when setup, controls, or engine-specific notes are non-obvious and would clutter `REPORT.md`
- No production code may reference or import from `prototypes/`
- Prototypes must not modify files outside `prototypes/`
- Prototypes must not be deployed or shipped

## When a Prototype Succeeds
If a prototype validates a concept and the feature moves to production:
1. The prototype code is NOT migrated directly — it is rewritten to production standards
2. The prototype `REPORT.md` findings inform the production design document or systems index
3. The prototype directory is preserved for reference but never extended

## Cleanup
Concluded prototypes should be archived or deleted only after findings are captured in `REPORT.md` and reflected in the relevant design docs when needed.
Never let prototype code grow into production code through incremental "cleanup."
