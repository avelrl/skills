# Systems Index: Courier Drift

## System List

| System | Category | Priority | Status | Design Doc | Depends On |
|--------|----------|----------|--------|------------|------------|
| Player Movement | Core | MVP | implemented | `design/gdd/player-movement.md` | Input |
| Combat Loop | Gameplay | MVP | implemented | `design/gdd/combat-loop.md` | Player Movement |
| Delivery Objective | Gameplay | MVP | identified | `design/gdd/delivery-objective.md` | Combat Loop |

## Integration Notes

- Player Movement and Combat Loop both exist as production modules, but they are not yet verified inside one coherent playable loop.
- The first playable still needs scene glue, objective pressure, HUD, restart flow, and an MVP assembly report before these systems can move to `integrated`.
