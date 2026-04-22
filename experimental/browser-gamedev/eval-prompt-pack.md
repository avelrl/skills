# Browser Game Eval Prompt Pack

Neutral prompt pack for manual runs, smoke evaluations, or future scenario fixtures.

These prompts are intentionally generic and IP-safe.
They are not canonical scenarios yet; use them as seeds for fixtures or exploratory testing.

## Prompt Set

### 1. Platformer: Lantern Courier

Target archetype: `platformer`

```text
Create a short side-view action platformer where a courier carries a fragile lantern through ruined rooftops during a storm.
The core loop is run, jump, avoid hazards, and stun a small number of rooftop enemies.
The first playable should prove movement feel, lantern readability, and one light combat interaction.
The style should be moody 2D pixel art with strong silhouettes and readable foreground hazards.
```

### 2. Top-Down: Salvage Runner

Target archetype: `top-down`

```text
Create a top-down sci-fi salvage game where the player dashes through a derelict station, collects energy cells, and escapes drone patrols.
The MVP should prove free movement, one dodge or dash action, and room-scale pressure from enemies or hazards.
The style should be clean neon industrial 2D with clear hazard color coding.
```

### 3. Grid Logic: Crystal Relay

Target archetype: `grid-logic`

```text
Create a grid-based puzzle game where the player reroutes crystal energy through a ruined machine by moving conductive blocks on a compact board.
The MVP should prove deterministic movement, readable state changes, and one clear solve condition.
The visual style should be stylized low-noise fantasy tech with a strong contrast between active and inactive cells.
```

### 4. Tower Defense: Lantern Garden

Target archetype: `tower-defense`

```text
Create a small tower defense game where spirit gardeners defend a lantern grove from night insects moving along visible garden paths.
The MVP should prove build-space clarity, 2-3 distinct tower roles, and one wave escalation that can both succeed and fail fairly.
The style should be soft 2D storybook art with readable projectiles and path edges.
```

### 5. UI Heavy: Academy Duel

Target archetype: `ui-heavy`

```text
Create a UI-heavy duel game where two academy rivals trade tactical cards and knowledge checks during a formal exam match.
The MVP should prove one onboarding scene, one complete duel loop, readable card choice feedback, and a clear win or loss outcome.
The style should be ornate but readable, with strong panel hierarchy and restrained animation.
```

## Good Uses

- quick manual archetype routing checks
- prompt seeds for fixture creation
- regression tests for `setup-engine`, `map-systems`, `design-system`, and browser-specific overlays

## Not Good Enough Yet

- final benchmark suites
- release-quality scenario packs
- deep asset-generation specifications

Promote only after the prompts produce stable, comparable workflow behavior across repeated runs.
