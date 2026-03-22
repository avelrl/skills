---
name: reverse-document
description: "Create technical documentation from existing implementation using the shared canonical templates."
argument-hint: "<type> <path> (technical-design|architecture)"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

Purpose: Recover shared technical documentation from existing implementation without inventing intent.

Use when:
- code exists first and a technical design or architecture doc is missing
- you need a defendable document based on implementation facts

Do not use for:
- speculative design before implementation
- game-system reverse docs that belong to `gamedev/`
- user-story or product requirement writing

Inputs / Required Context:
- required: `<type>` and a real code or module path
- read: target path plus nearby code, tests, configs, and relevant docs
- ask only for intent that cannot be recovered from implementation

Outputs / Owned Artifacts:
- owns `docs/design/[slug].md` for `technical-design`
- owns `docs/architecture/adr-[NNNN]-[slug].md` for `architecture`
- creates `docs/design/` or `docs/architecture/` if needed
- uses shared templates only

Modes or Arguments:
- `technical-design|design <path>`
- `architecture <path>`

Execution Rules:
1. Validate the type and target path.
2. Read only the material needed to document responsibilities, interfaces, data flow, dependencies, edge cases, and constraints.
3. Add a short reverse-documentation context near the top of the doc.
4. For architecture outputs, determine the next ADR number before saving.
5. Save the result to the canonical shared path.

Failure / Stop Conditions:
- stop if the path does not exist or the type is unsupported
- stop and redirect if the request is actually a game-system design doc
- if rationale cannot be proven, mark it as inferred or open instead of pretending certainty

Return Format:
- source path
- output path
- what is now documented
- what is still inferred or unresolved
- what should be reviewed next

Example Invocation:
- `/reverse-document technical-design src/auth/refresh.go`

Related Skills / Boundary:
- use `architecture-decision` when the main task is making or updating an ADR
- do not pull game-specific templates or rules into this shared skill
