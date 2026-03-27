# Systems Index: Courier Drift

**Closure State**: Stable MVP

## System List

| System | Category | Priority | Status | Design Doc | Depends On |
|--------|----------|----------|--------|------------|------------|
| Player Movement | Core | MVP | integrated | `design/gdd/player-movement.md` | Input |
| Combat Loop | Gameplay | MVP | integrated | `design/gdd/combat-loop.md` | Player Movement |
| Delivery Objective | Gameplay | MVP | integrated | `design/gdd/delivery-objective.md` | Combat Loop |

## Integration Notes

- Player Movement and Combat Loop are already wired into one first-playable scene with boot flow, HUD, fail states, relay-gate pressure, and restart flow.
- Delivery Objective is already present in the current runtime through the relay gate and countdown flow.
- One successful evidence run exists, but the latest failed rerun has not yet been folded back into this closure state.

## Progress Snapshot

| Metric | Value |
|--------|-------|
| Integrated MVP systems | 3 |
| Current closure state | `Stable MVP` |
| Repeatability evidence | mixed; latest rerun still needs closure sync |

## Next Steps

- [x] Keep the runtime slice coherent and reproducible.
- [ ] Reconcile the mixed repeatability evidence with the current closure claim.
