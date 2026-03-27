# Systems Index: Courier Drift

**Closure State**: Playable

## System List

| System | Category | Priority | Status | Design Doc | Depends On |
|--------|----------|----------|--------|------------|------------|
| Player Movement | Core | MVP | integrated | `design/gdd/player-movement.md` | Input |
| Combat Loop | Gameplay | MVP | integrated | `design/gdd/combat-loop.md` | Player Movement |
| Delivery Objective | Gameplay | MVP | integrated | `design/gdd/delivery-objective.md` | Combat Loop |

## Integration Notes

- Player Movement and Combat Loop are already wired into one first-playable scene with boot flow, HUD, fail states, relay-gate pressure, and restart flow.
- Delivery Objective is already present in the current runtime through the relay gate and countdown flow, but the canonical closure wording has not been updated to match the accepted reports.
- The next skill is whichever closure-sync step reconciles the current evidence; do not add new systems unless a real blocker reappears.

## Progress Snapshot

| Metric | Value |
|--------|-------|
| Integrated MVP systems | 3 |
| Current closure state | `Playable` |
| Canonical docs requiring closure sync | `README.md`, `reports/mvp-assembly-report.md`, `reports/playtest-report.md`, relevant system GDDs |

## Next Steps

- [x] Keep the runtime slice coherent and reproducible.
- [ ] Sync closure docs to the accepted playtest read without broadening scope.
