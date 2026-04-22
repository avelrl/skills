---
name: implement-system
description: "Implement one approved game system in production-facing project code."
argument-hint: "<system-name>"
user-invocable: true
---

Purpose: Turn one approved system design into integrated project code without expanding scope beyond that system.

Use when:
- `design/gdd/[system-name].md` exists and the project scaffold already exists
- the team wants one real gameplay or support system added to the main codebase
- prototype or design evidence is clear enough to support production-facing implementation

Do not use for:
- writing the system GDD
- building a disposable spike in `prototypes/`
- integrating multiple unfinished systems into a playable loop at once

Inputs / Required Context:
- required: `design/gdd/[system-name].md`
- required: project scaffold and runnable entrypoint
- optional: `docs/technical-preferences.md`, `design/gdd/game-concept.md`, `design/gdd/systems-index.md`, `design/gdd/asset-registry.md`, related upstream or downstream system docs, `gamedev/standards/gameplay-code.md`, and `gamedev/standards/data-files.md`

Outputs / Owned Artifacts:
- owns production-facing implementation for the requested system in the main project code
- may add or update data files, tests, configuration, and minimal placeholder assets required by the system
- may update `design/gdd/systems-index.md` so implementation status reflects reality
- may update the target GDD status block and acceptance criteria so canonical docs match the implementation

Modes or Arguments:
- `<system-name>`: normalized to the matching GDD file and code concern

Execution Rules:
1. Read the target system GDD first and summarize the non-negotiable rules, interfaces, and assumptions.
2. Stop and route to `design-system` if the target GDD does not exist.
3. Stop and route to `bootstrap-project` if there is no runnable scaffold yet.
4. Read only the surrounding project context needed to integrate the system cleanly, plus shared gameplay or data standards when they are relevant.
5. Before editing code, write a brief file-level implementation plan naming the files you expect to create or update, the main interfaces or hooks you will touch, and the verification target you expect to run.
6. When the chosen runtime already has specialist implementation guidance, follow that guidance instead of inventing a parallel local convention in generic `gamedev/` text.
7. When the system depends on concrete asset keys, runtime asset paths, or placeholder swaps, read `design/gdd/asset-registry.md` when it exists and keep new references aligned with it.
8. Implement the smallest production-facing version of the system that satisfies the GDD and current MVP scope.
9. Prefer simple data flows, explicit state, and obvious seams over premature abstraction.
10. Add or update tests where the repository stack supports them; if tests are not yet practical, document the gap explicitly.
11. Run the narrowest relevant verification command the repository supports, such as a unit test, build, or local smoke entrypoint, and record the actual command or explicit blocker.
12. Update `design/gdd/systems-index.md` when present so status reflects the strongest confirmed state:
   - use `implemented` when production code exists but the system is not yet verified in the main playable loop
   - never downgrade `integrated`
13. Update the target GDD status block to match reality:
   - use `Implemented` for `Document Status` when production code now exists but main-loop verification is still pending
   - if the system is already verified in the main playable loop, use `Integrated`
   - keep `System Index Status` aligned with the strongest confirmed systems-index state
14. If one or more GDD acceptance criteria are now satisfied, check them or rewrite them so the document does not lag behind the code.
15. Record doc mismatches as assumptions or follow-up work instead of silently redesigning the system in code.
16. End with the next handoff in the flow: another `implement-system`, `assemble-mvp`, or `playtest-and-tune`.

Failure / Stop Conditions:
- stop if the target system GDD does not exist
- stop if the request really needs a throwaway prototype instead of production-facing code
- stop if implementing the requested system would force multiple unrelated systems to be invented first
- do not silently redesign the system while coding; record mismatches as assumptions or follow-up work

Return Format:
- implemented system name
- file-level implementation plan actually used
- key files created or updated
- tests added or skipped
- systems-index status update and rationale
- assumptions or gaps left open
- next recommended skill: `implement-system`, `assemble-mvp`, or `playtest-and-tune`

Example Invocation:
- `/implement-system player-movement`
- `/implement-system combat-loop`

Related Skills / Boundary:
- use `design-system` before this skill to define the system contract
- use `prototype` before this skill when risk is still too high
- use `assemble-mvp` after a few core systems are implemented and need glue
- use `playtest-and-tune` after a coherent playable slice exists
