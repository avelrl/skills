# Gamedev Quickstart

One-page prompt sheet for the most common `gamedev` starting points.

## Always State The Language Policy Early

Use this shape in the first substantial prompt:

```text
Game idea: ...
Working/documentation language: Russian.
Player-facing language(s): English and Russian.
Current milestone: concept.
Choose and produce the next correct gamedev artifact.
```

## Ready Prompts

### 0. I only have a concept, but I want the first GDD

```text
I only have `design/gdd/game-concept.md`.
Do not jump straight to `/design-system`.
First use `/setup-engine`.
Then use `/map-systems`.
After that, recommend which system should get the first `/design-system`.
Working/documentation language: Russian.
Player-facing language(s): English.
```

Expected route: `/setup-engine` -> `/map-systems` -> first `/design-system`

### 1. I only have an idea

```text
Create design/gdd/game-concept.md for a small top-down action game.
Working/documentation language: Russian.
Player-facing language(s): English.
Then continue with the nearest correct gamedev step only.
```

Expected start: `setup-engine` after the concept exists.

### 2. I do not know the stack

```text
Use `/setup-engine`.
Pick the stack for this game and write docs/technical-preferences.md.
Working/documentation language: Russian.
Player-facing language(s): English.
Target platforms: Web first, Unity as a future port lane.
```

Expected start: `setup-engine`

### 3. I need the systems map

```text
Use `/map-systems`.
Break this game into systems and update design/gdd/systems-index.md.
Keep the documentation in Russian.
Keep player-facing terms aligned with English UI copy.
```

Expected start: `map-systems`

### 4. I need one system GDD

```text
Use `/design-system combat-loop`.
Write the combat system GDD in Russian.
Player-facing language is English.
Use the existing systems index and do not implement code.
```

Expected start: `design-system`

### 5. I need to test one risky mechanic

```text
Use `/prototype`.
Prototype the dash mechanic and check whether the combat loop still reads clearly.
Do not touch production code.
Write the result as a prototype report.
```

Expected start: `prototype`

### 6. I need the first playable

```text
Use `/assemble-mvp`.
Assemble the smallest real playable loop from the implemented systems.
Do not broaden scope.
Write the MVP assembly report and then recommend the next step.
```

Expected start: `assemble-mvp`

### 7. The MVP works, now I need a real demo

```text
Use `/prepare-demo`.
Prepare the first audience-facing demo from the current playable slice.
This is not a UI-only request.
Define the demo-critical gameplay, onboarding, HUD, menu, placeholder, asset, and QA gaps.
Write reports/demo-readiness.md and recommend the next step.
```

Expected start: `prepare-demo`

### 8. The UI fell apart after MVP

```text
The core loop exists, but the presentation layer is not demo-ready.
Run the nearest correct workflow step.
Do not jump straight into random UI implementation.
```

Expected start: usually `prepare-demo`

### 9. I need a visual contract before buying, generating, or importing assets

```text
Create or update `design/gdd/art-bible.md` from `gamedev/templates/art-bible.md`.
Keep it concise and practical for a small team.
Capture palette, silhouette rules, UI density, VFX direction, animation expectations, asset naming, and which placeholders are acceptable for the next milestone.
Do not turn this into lore or a giant asset backlog.
```

Expected start: explicit artifact request, usually near `prepare-demo` or before broader asset production
