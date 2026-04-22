# Browser Gamedev Overlays

Optional browser-specific overlays for web game work.

These notes are intentionally outside the canonical `gamedev/` path.
They are useful when a project is explicitly browser-first and the team wants extra depth for archetype choice, browser debugging, or eval prompt design.

These files are reference notes, not standalone skills.
They should be used alongside the existing repo skills, not instead of them.

Use these files as overlays:

- [`archetypes.md`](archetypes.md): browser-friendly archetype shortcuts and failure modes
- [`browser-debug-checklist.md`](browser-debug-checklist.md): practical browser game validation checklist
- [`eval-prompt-pack.md`](eval-prompt-pack.md): neutral prompts for manual runs and future eval fixtures

Boundaries:

- Keep `docs/technical-preferences.md`, `design/gdd/`, reports, and workflow routing in the canonical `gamedev/` flow.
- Use `Game Studio` or another browser specialist for runtime-specific implementation depth when available.
- Treat this folder as working guidance, not as a replacement for specialist docs or engine-native docs.

## How To Use With Skills

### 1. During Stack Choice

Use:

- primary skill: `gamedev/setup-engine`
- optional overlay: [`archetypes.md`](archetypes.md)

Why:

- `setup-engine` still owns `docs/technical-preferences.md`
- `archetypes.md` helps you classify the browser game before deeper design

### 2. During Systems Mapping And GDD Work

Use:

- primary skills: `gamedev/map-systems`, `gamedev/design-system`
- optional overlay: [`archetypes.md`](archetypes.md)

Why:

- the overlay helps sharpen what kind of browser game you are actually building
- the canonical artifacts still belong in `design/gdd/`

### 3. During Browser QA Or Playable Debugging

Use:

- primary skills: `core/web-ui-smoke`, `core/web-ui-doctor`
- optional overlay: [`browser-debug-checklist.md`](browser-debug-checklist.md)

Why:

- the skills perform the actual browser work
- the checklist helps you avoid random guessing and cover browser-game-specific failure modes

### 4. During Eval Or Prompt Design

Use:

- primary doc: `docs/gamedev-autoimprovement.md`
- optional overlay: [`eval-prompt-pack.md`](eval-prompt-pack.md)

Why:

- the main eval design still lives in the canonical docs
- the prompt pack is only a browser-game scenario seed

## Example Use

Example browser-first route:

1. Run `gamedev/setup-engine` for the stack decision.
2. Consult [`archetypes.md`](archetypes.md) if the gameplay type is still fuzzy.
3. Run `gamedev/map-systems`.
4. Run `gamedev/design-system` for the first browser-game system.
5. Use `core/web-ui-smoke` for local browser validation.
6. Consult [`browser-debug-checklist.md`](browser-debug-checklist.md) if the game boots but behaves badly.

Promotion rule:

- If one of these overlays proves useful across several real browser projects, move the stable parts into `docs/` or `gamedev/`.
