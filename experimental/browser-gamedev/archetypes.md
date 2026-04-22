# Browser Game Archetypes

Optional browser-game archetype guide for quick classification and downstream planning.

This file is useful when a web game concept is still fuzzy and the team needs a short-hand view of likely design and implementation pressure before deeper specialist work begins.

## Quick Classifier

| Archetype | Core Question | Typical Camera / Space | Main Design Pressure | Common Browser Risk |
|-----------|---------------|------------------------|----------------------|---------------------|
| Platformer | Does the player fall and jump under gravity? | Side-view, lane-based traversal | Movement feel, collision clarity, combat timing | Janky jump feel, collider drift, unreadable telegraphs |
| Top-Down | Can the player move freely in all directions without jumping? | Overhead or angled top-down | Spatial navigation, enemy pressure, readability | Weak encounter density, cluttered bullets, pathing chaos |
| Grid Logic | Does state advance on discrete grid steps or turns? | Board, lane, cell, or tile grid | Rule clarity, puzzle state, deterministic feedback | Ambiguous state changes, hard-to-read cells, accidental animation noise |
| Tower Defense | Do enemies follow lanes or paths while the player places defenses? | Map overview with path ownership | Lane clarity, upgrade economy, wave pacing | Path unreadability, over-busy FX, build-space confusion |
| UI Heavy | Is most of the experience driven by dialogue, cards, HUD, panels, or menus rather than spatial action? | Screen-space presentation | Information hierarchy, pacing, onboarding, feedback | Modal chaos, stale state, hidden interaction priority |

## Platformer

Use when:

- jumping, fall timing, ledge risk, or side-view combat are central
- level structure matters more than free exploration

Design emphasis:

- movement baseline first: walk, jump, air control, coyote or buffer windows if needed
- keep encounter shapes legible at the same scale as the traversal route
- prefer a small number of enemy and hazard types in MVP

Implementation bias:

- lock camera and collision rules early
- treat traversal and combat as separate systems in `design/gdd/`
- store risky movement experiments under `prototypes/`

Typical proof:

- one short level where movement and one combat interaction both feel stable

## Top-Down

Use when:

- the player needs full directional movement
- dodge, chase, circle-strafe, exploration, or room pressure matter more than platform timing

Design emphasis:

- enemy density and room readability
- input responsiveness under continuous movement
- visual prioritization for hazards, pickups, and the player avatar

Implementation bias:

- map space and combat readability should be designed together
- avoid broad enemy variety before one clean encounter loop exists
- capture spawn, wave, or room pacing as explicit tuning knobs

Typical proof:

- one repeatable room or arena with stable spawn pressure and readable hazards

## Grid Logic

Use when:

- state changes should feel deterministic and step-based
- puzzle clarity matters more than animation spectacle

Design emphasis:

- exact rules for turns, pushes, swaps, matches, or occupancy
- immediate feedback for legal versus illegal moves
- compact level or board goals

Implementation bias:

- document formulas and edge cases early
- use deterministic data updates before polish animation
- verify restart and undo-like flows if they matter to the concept

Typical proof:

- one board or puzzle slice that can be solved cleanly without rule ambiguity

## Tower Defense

Use when:

- route ownership, build slots, upgrade choices, and wave timing define the core loop

Design emphasis:

- path clarity at a glance
- tower role separation
- economy pacing and failure recovery

Implementation bias:

- route, build-space, and wave systems should be explicit in the systems index
- keep projectile readability above spectacle
- record placeholder policy for towers, enemies, and impact FX before demo work

Typical proof:

- one lane or small map with 2-3 tower roles and at least one losing state that feels fair

## UI Heavy

Use when:

- most player decisions happen through cards, dialogue, menus, modals, or narrative pacing
- the spatial runtime exists mainly to support presentation and state flow

Design emphasis:

- hierarchy of what the player must read next
- turn, chapter, or panel flow
- explanation, onboarding, and reset behavior

Implementation bias:

- model scene and state transitions carefully
- treat HUD and modal layering as first-class implementation concerns
- keep copy, choice effects, and content data explicit instead of burying them in scene code

Typical proof:

- one complete interaction loop from onboarding to outcome with no hidden state confusion

## What To Hand Off Next

- Use `setup-engine` to lock the stack.
- Use `map-systems` to turn the archetype into named systems instead of vague feature wishes.
- Use `design-system` to write one system contract at a time.
- Use `prepare-demo` before broad polish if the milestone shifts from “prove the loop” to “show a credible build”.
