# Courier Drift - Focused Playtest Report

## Status

- **Report Path**: `reports/playtest-report.md`
- **Date**: 2026-03-25
- **Focus Area**: closure repeatability
- **Build or Run Target**: `npm install && npm run dev`
- **Outcome**: Mixed
- **Closure Recommendation**: Playable until repeatability is proven

## Baseline Observations

- The first successful rerun (`reports/evidence/repeatability-success-run-01.json`) supported the stronger closure claim.
- A later rerun (`reports/evidence/repeatability-failed-rerun.json`) did not reproduce that success, so the closure state is not durable yet.

## Changes Made

- No new tuning change was accepted in this fixture state.
- The real issue is honest closure classification, not another round of value churn.

## Re-test Observations

- One success artifact exists, but the latest rerun failed to reproduce the same extraction closure.
- The playable slice still exists, so the correct downgrade is closure state, not system integration.

## What Improved

- The current evidence set now makes the closure-risk explicit instead of hiding behind one successful run.

## What Still Feels Off

- Top-level closure docs still overstate the current state as `Stable MVP`.
- The current accepted read should stay at `Playable` until repeatable success is proven.

## Design Sync

- **Relevant Docs**: `README.md`, `reports/mvp-assembly-report.md`, `design/gdd/systems-index.md`, `design/gdd/player-movement.md`, `design/gdd/combat-loop.md`, `design/gdd/delivery-objective.md`
- **Defaults Adopted**: `relay_deadline_seconds 55`; `enemy telegraph alpha 0.72`; `overlay contrast variant high`
- **Follow-Up Needed**: sync the canonical closure docs down to the accepted `Playable` read until repeatable success is proven

## Recommendation

- **Continue tuning**: Yes, but only if the team wants to re-attempt stable closure after another focused rerun.
- **Route to implementation**: None
- **Route to redesign**: None
