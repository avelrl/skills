# Experimental Material

This directory holds optional or trial material that may be useful in real work but is not part of the canonical repo flow yet.

Rules:

- Do not treat `experimental/` as the default entrypoint.
- Do not let experimental notes override `docs/`, `core/`, `gamedev/`, `templates/`, or `standards/`.
- Promote material into the main contour only after it proves useful across multiple runs.

Current focus:

- `browser-gamedev/` for browser-specific overlays inspired by external research, without turning the main `gamedev/` path into a browser-only system

## What This Is

These files are reference notes and trial workflow material.
They are not standalone skills and they do not replace the main repo flow.

Use them when:

- the normal `gamedev/` flow is already the right route
- the project has an explicit browser-game angle
- you want extra guidance for browser archetypes, browser debugging, or future eval prompts

Do not use them as:

- a shortcut around `setup-engine`, `map-systems`, `design-system`, or other canonical steps
- a replacement for `core/web-ui-smoke`, `core/web-ui-doctor`, or runtime specialists

## How To Use With Skills

1. Start with the normal skill from `gamedev/`.
2. Open the relevant experimental note only if it adds browser-specific depth.
3. Keep the owned project artifacts in the canonical locations such as `docs/technical-preferences.md`, `design/gdd/`, and `reports/`.

Typical pairing:

- stack and runtime choice:
  - primary skill: `gamedev/setup-engine`
  - optional overlay: `experimental/browser-gamedev/archetypes.md`
- systems mapping or first system design for a browser game:
  - primary skills: `gamedev/map-systems`, `gamedev/design-system`
  - optional overlay: `experimental/browser-gamedev/archetypes.md`
- browser QA or local web-game debugging:
  - primary skills: `core/web-ui-smoke`, `core/web-ui-doctor`
  - optional overlay: `experimental/browser-gamedev/browser-debug-checklist.md`
- shaping browser-game eval scenarios:
  - primary doc: `docs/gamedev-autoimprovement.md`
  - optional overlay: `experimental/browser-gamedev/eval-prompt-pack.md`

## Quick Route

- If the project is not explicitly browser-first, ignore this directory.
- If the project is browser-first but the main issue is workflow routing, stay in `gamedev/`.
- If the project is browser-first and you need extra browser-specific guidance, use the matching file under `browser-gamedev/`.
