# Systems Index: Courier Drift

## System List

| System | Category | Priority | Status | Design Doc | Depends On |
|--------|----------|----------|--------|------------|------------|
| Player Movement | Core | MVP | integrated | `design/gdd/player-movement.md` | Input |
| Combat Loop | Gameplay | MVP | integrated | `design/gdd/combat-loop.md` | Player Movement |
| Delivery Objective | Gameplay | MVP | identified | `design/gdd/delivery-objective.md` | Combat Loop |

## Integration Notes

- Player Movement and Combat Loop are already wired into one first-playable scene with boot flow, HUD, fail states, relay-gate pressure, and restart flow.
- Delivery Objective remains `identified`; the current relay gate and countdown are MVP glue, not a separately approved system implementation.
- The next skill is `playtest-and-tune`, not more assembly, unless the build fails to boot in the target environment.
