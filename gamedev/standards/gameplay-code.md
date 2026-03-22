---
paths:
  - "src/gameplay/**"
---

# Gameplay Code Rules

- Keep gameplay logic separate from UI and presentation glue.
- Externalize balance-sensitive values into data files or clearly owned config.
- Use explicit states and transitions for systems with non-trivial lifecycle.
- Prefer interfaces and events over hard references between gameplay systems.
- Make core gameplay logic testable without the full runtime loop when practical.
- Treat global mutable game state as a last resort.
- When a feature implements a design doc, keep the mapping obvious in code or adjacent docs.
