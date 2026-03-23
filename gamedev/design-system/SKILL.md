---
name: design-system
description: "Write or update a game-system GDD using the canonical gamedev template."
argument-hint: "<system-name>"
user-invocable: true
---

Purpose: Write or update one game-system GDD from the approved systems map.

Use when:
- a system already exists in `design/gdd/systems-index.md`
- the project needs one implementable GDD for that specific system

Do not use for:
- creating the overall systems index
- inventing the game concept
- broad stage or project health analysis

Inputs / Required Context:
- required: `design/gdd/game-concept.md` and `design/gdd/systems-index.md`
- optional: `design/gdd/game-pillars.md`, existing `design/gdd/[system-name].md`, upstream or downstream system docs, relevant prototype reports in `prototypes/*/REPORT.md`, `gamedev/standards/design-docs.md`

Outputs / Owned Artifacts:
- owns `design/gdd/[system-name].md`
- updates the matching row in `design/gdd/systems-index.md`
- uses `gamedev/templates/game-design-document.md`

Modes or Arguments:
- `<system-name>`: normalized to kebab-case for the target GDD path

Execution Rules:
1. Parse the system name and validate that the concept and systems index exist.
2. Stop and route to `map-systems` if `design/gdd/systems-index.md` is missing.
3. Stop and refresh the systems index if the requested system is not present there.
4. Summarize the system's layer, priority, dependencies, interfaces, formulas, assumptions, and existing evidence.
5. Create or update `design/gdd/[system-name].md` using the canonical GDD template and shared design-doc rules.
6. Ensure the `Scope Boundaries` section clearly separates:
   - `In MVP`
   - `In Vertical Slice`
   - `Deferred / Later`
7. If a relevant prototype report exists, keep an explicit `Evidence / Prototype Inputs` section that:
   - references the report path or paths
   - extracts up to 4 key findings
   - records adopted baseline values or `None adopted yet`
   - records remaining open questions or evidence gaps
8. If no relevant prototype exists, keep the section and explicitly mark `None yet` instead of implying certainty.
9. Update the matching row in `design/gdd/systems-index.md` so status reflects the strongest confirmed state.
10. When syncing status:
   - use `designed` when the GDD exists but prototype findings are not yet folded into it
   - use `informed-by-prototype` when prototype findings and baseline decisions are reflected in the GDD
   - never downgrade `implemented` or `integrated`
11. If prototype evidence changes scope or assumptions, rewrite the affected sections so the document stays internally consistent instead of appending contradictory notes.
12. When the GDD is implementation-ready and the scaffold already exists, end with a handoff to `implement-system`; otherwise hand off to another `design-system` or `prototype`.

Failure / Stop Conditions:
- stop if the game concept is missing
- stop if the requested system is outside the current systems index
- record unknowns as assumptions or open questions instead of inventing detail

Return Format:
- GDD path
- systems-index status update and rationale
- scope boundaries captured
- key rules or decisions captured
- evidence adopted from prototype reports, if any
- open questions that still block implementation
- next recommended skill: `design-system`, `prototype`, or `implement-system`

Example Invocation:
- `/design-system combat-loop`

Related Skills / Boundary:
- use `map-systems` to define the system list before writing GDDs
- use `prototype` when one mechanic is still too risky to spec confidently
- use `implement-system` once the GDD is stable and a runnable project scaffold exists
