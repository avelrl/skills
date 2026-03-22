---
name: architecture-decision
description: "Create or update an ADR using the shared canonical template."
argument-hint: "<title>"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

Purpose: Create or update one ADR using the canonical shared template.

Use when:
- a technical or operational decision has lasting architectural impact
- the team needs one canonical record of problem, options, trade-offs, and outcome

Do not use for:
- routine implementation notes
- general technical design docs
- game-system GDD work

Inputs / Required Context:
- required: a concrete decision title
- read: relevant code, existing ADRs, nearby design or operational docs
- clarify only: problem, serious alternatives, constraints, migration concerns, decision status

Outputs / Owned Artifacts:
- owns `docs/architecture/adr-[NNNN]-[slug].md`
- creates `docs/architecture/` if it does not exist
- uses `templates/architecture-decision-record.md`

Modes or Arguments:
- `<title>`: concrete decision title

Execution Rules:
1. Validate the title and normalize the slug.
2. Determine the next ADR number by scanning `docs/architecture/`.
3. Distinguish `proposed` from `reverse-documented` decisions.
4. Read only the source material needed to defend the trade-offs.
5. Draft the ADR and save it to the canonical path.

Failure / Stop Conditions:
- stop if the title remains vague after one clarification
- stop if no defendable problem, options, or trade-off can be recovered
- record uncertainty explicitly instead of inventing historical certainty

Return Format:
- ADR path
- decision status: `proposed` or `reverse-documented`
- main trade-offs
- riskiest follow-up work

Example Invocation:
- `/architecture-decision adopt-postgres-logical-replication`

Related Skills / Boundary:
- use `reverse-document` when the main task is documenting existing implementation
- do not expand this skill into a general technical design workflow
