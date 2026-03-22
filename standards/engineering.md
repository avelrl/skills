# Engineering Standard

Use this as the shared baseline across projects and domains.

## Code

- Optimize for clear ownership, explicit interfaces, and predictable data flow.
- Document non-obvious public contracts and behavior that callers must rely on.
- Avoid hidden coupling, ambient global state, and irreversible side effects in shared code.
- Put project-specific decisions in project docs; keep shared code and shared standards generic.

## Documentation

- Write the smallest document that removes real ambiguity.
- Every design or technical spec should state scope, dependencies, edge cases, and acceptance criteria.
- Templates are fill-in skeletons; standards define quality bars; workflow docs define process. Do not mix them.
- Use ADRs for decisions that affect architecture, interfaces, migration, or long-term maintenance cost.

## Delivery

- Verification is required before marking work done: tests, checks, screenshots, or another concrete proof.
- A bug fix should include the missing check or regression coverage when practical.
- If a workflow depends on assumptions that cannot be verified automatically, call them out explicitly instead of pretending certainty.
