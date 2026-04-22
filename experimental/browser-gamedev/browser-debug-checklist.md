# Browser Game Debug Checklist

Browser-specific validation checklist for local web games.

Use this as an overlay when a project is already browser-first and the main issue is runtime sanity, integration drift, or browser QA depth.
Do not pull these expectations into generic `gamedev/` by default.

## Preflight

- Confirm the actual run target and URL.
- Confirm the intended verification order: build, smoke, interactive pass, restart pass.
- Confirm which scene, menu, or loop is the current proof target.
- Confirm where screenshots, logs, or smoke artifacts should be saved.

## Static Consistency Checks

Before blaming the browser, check these first:

- every boot target, route, or first playable scene is still registered where the runtime expects it
- asset keys or file paths referenced by code and data still exist
- config fields used by gameplay code still exist at the expected path
- placeholder assets that were supposed to be replaced are not still wired into the core path
- player input hints match actual bindings
- UI overlays, DOM HUD, canvas HUD, and modal layers are not fighting for top priority
- scene restart or route restart resets mutable state instead of reusing stale values

## Run Order

1. Run the narrowest build or typecheck the repo supports.
2. Start the app and verify reachability with a simple HTTP check.
3. Run a real browser smoke path.
4. Inspect console, page, and request errors before touching gameplay tuning.
5. Restart the same flow from the title or menu and make sure state resets cleanly.
6. If the build claims mobile support or responsive UI matters, run one mobile-sized sanity pass before calling the slice stable.

## Gameplay-Specific Checks

### Readability

- the player avatar is always visually dominant enough to track
- hostile effects, damage zones, and interactables are distinguishable at gameplay speed
- feedback on hit, pickup, fail, success, or blocked action happens fast enough to teach the rule

### State Integrity

- pause, restart, death, retry, or scene re-entry do not leave duplicate listeners or stacked UI
- counters, timers, score, combo, wave, or turn state reset when a new run begins
- tutorial prompts and onboarding gates do not reappear forever after the player has already cleared them, unless that is intended

### Presentation Integrity

- title, menu, HUD, and fail-state flows all lead somewhere valid
- placeholder copy, missing icons, empty buttons, or broken images are called out as product issues, not just cosmetic notes
- if DOM UI is layered over canvas, focus and pointer routing still work after transitions

## Failure Signatures

| Symptom | Likely Cause | First Check |
|---------|--------------|-------------|
| Blank page with no obvious error | Broken entrypoint, missing route, fatal boot exception | Browser console and app boot target |
| Game boots but start flow fails | First playable scene or menu target drifted | Startup route, scene registration, restart path |
| Visuals load but interaction is dead | Focus lost, overlay capturing input, stale state | Active modal layer, input binding, event listener cleanup |
| Some assets are missing | Key drift, import path drift, placeholder removal without replacement | Asset registry, file paths, runtime asset references |
| Retry works once then breaks | Mutable state survives restart | Cleanup and reset logic for timers, listeners, registries |
| HUD is technically present but unreadable | Layering, scale, typography, contrast, or pacing issue | One focused screenshot and readable-state pass |
| Works in desktop but not mobile size | Layout assumptions depend on large viewport | Responsive pass at the intended mobile target |

## Evidence To Keep

- one final screenshot of the main proof path
- the exact run target used
- the smoke artifact directory, if one was produced
- any console or request failures that still matter after the final pass

## Escalation Rule

If the browser itself cannot launch or local reachability is unstable, stop guessing and switch to the repo's browser-doctor flow instead of treating it like a gameplay bug.
