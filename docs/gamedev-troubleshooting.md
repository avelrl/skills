# Gamedev Troubleshooting

Common `gamedev` workflow problems and the nearest correct route.

| Problem | Likely issue | Nearest correct step |
|---------|--------------|----------------------|
| I only have an idea and no project files yet. | The project is still at concept stage. | Write `design/gdd/game-concept.md`, then run `setup-engine`. |
| I do not know whether to prototype or implement. | The risk vs approved-design split is unclear. | Use `prototype` for uncertainty, `implement-system` for approved GDD-backed work. |
| Codex started coding before the design was stable. | The request sounded like implementation, not design. | Route back to `map-systems` or `design-system`. |
| The build does not boot, but I asked for a playtest. | There is no real playable baseline yet. | Route back to `assemble-mvp` or `implement-system`. |
| The MVP exists, but the UI or presentation layer feels broken. | The problem is demo readiness, not just tuning. | Usually run `prepare-demo`, then `design-system` or `implement-system`. |
| I need a demo, not just an MVP. | The repo has proven the loop, but not the audience-facing contract. | Run `prepare-demo`. |
| Docs started mixing Russian and English randomly. | The language policy was never fixed clearly or drifted later. | Update `design/gdd/game-concept.md` and `docs/technical-preferences.md`, then sync downstream docs. |
| Codex tries to do too much in one pass. | The prompt sounded like a full-run request. | Name the exact step you want, such as `design-system combat-loop` or `implement-system hud`. |

## Quick Reality Checks

- If the loop does not run, you are not at `playtest-and-tune` yet.
- If the system is not approved in docs, you are not at `implement-system` yet.
- If the MVP already runs but the milestone changed to `show this to people`, you are probably at `prepare-demo`.
- If the question is still `is this mechanic even good`, you are probably at `prototype`.
