---
name: web-ui-smoke
description: "Use when Codex needs to run a local web app in a real browser, click/fill/press, wait for visible UI changes, save screenshots, and inspect console/page/request errors. Best default for browser smoke tests across repos."
argument-hint: "<url-or-local-app>"
user-invocable: true
---

# Web UI Smoke

Use this skill as the default browser hammer for ordinary local web apps.
It is repo-agnostic: the reusable browser runner lives in the skill, while each repo only needs a way to start its own app.

## Use when

- Codex needs to open a local web page and exercise it like a user
- the task includes clicks, fills, key presses, waits, screenshots, or basic UI assertions
- the repo does not already have a good E2E suite, or you need a lightweight smoke loop before writing one
- you want artifacts saved in the repo while keeping the Playwright client global

## Do not use for

- diagnosing sandbox, trust, dependency-install, or browser-launch failures from first principles; use `web-ui-doctor`
- canvas/game-specific flows that require `render_game_to_text` and deterministic stepping; use `develop-web-game`
- replacing an existing repo E2E suite if the project already has a stable `@playwright/test` setup

## Skill paths

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEB_UI_CLIENT="$CODEX_HOME/skills/web-ui-smoke/scripts/web_ui_playwright_client.js"
export WEB_UI_ACTIONS="$CODEX_HOME/skills/web-ui-smoke/references/actions.example.json"
export WEB_UI_SMOKE_RUNNER="$CODEX_HOME/skills/web-ui-smoke/scripts/run_smoke.sh"
export WEB_UI_SMOKE_RUNTIME_INFO="$CODEX_HOME/skills/web-ui-smoke/scripts/runtime_info.sh"
export WEB_UI_SMOKE_RUNTIME_DIR="${WEB_UI_SMOKE_RUNTIME_DIR:-$CODEX_HOME/runtimes/web-ui-smoke}"
```

These exports are reference values, not the preferred approval-sensitive invocation form.
When command-prefix approval reuse matters, resolve the installed absolute script path first and execute that literal path directly.
Do not launch the wrapper via `"$HOME/.codex/..."`, `"$CODEX_HOME/..."`, `"$WEB_UI_SMOKE_RUNNER"`, or an env-prefixed command if a stable direct path already exists.

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).
Runtime dependencies live separately under `$CODEX_HOME/runtimes/web-ui-smoke`.
If `CODEX_HOME` points at a repo-local `.codex`, this means the runtime will live under `.codex/runtimes/`.
That is acceptable support material; the important rule is to keep runtime files out of `.codex/skills/`.
For ordinary manual runs, prefer the default home-level runtime and do not override `WEB_UI_SMOKE_RUNTIME_DIR` to a repo-local path unless you explicitly want an isolated disposable runtime.

## One-time runtime install

```bash
/absolute/path/to/.codex/skills/web-ui-smoke/scripts/install_runtime.sh
```

This install belongs to the shared smoke runtime, not the target repo and not the skill snapshot.
For approval reuse, prefer the literal installed script path here too.
Do not satisfy a missing Playwright import by creating repo-local shims such as `node_modules/playwright`,
installing dependencies under `.codex/skills/web-ui-smoke`, symlinking random global bundles, or hardcoding browser-cache executables.

## Wrapper scripts

Prefer the wrapper scripts over raw `node ...` commands.
They keep approval requests shorter and make persistent command-prefix approval practical.
Prefer direct execution of the script path over `bash /path/to/script.sh`.
For ordinary manual runs that already use the default home runtime, do not pass `--runtime-dir`.
That flag is mainly for intentional isolation or explicit doctor comparisons.

- smoke runner: `"$WEB_UI_SMOKE_RUNNER" ...`
- runtime info probe: `"$WEB_UI_SMOKE_RUNTIME_INFO" ...`
- preferred approval-friendly form: `/absolute/path/to/.codex/skills/web-ui-smoke/scripts/run_smoke.sh ...`
- preferred approval-friendly probe: `/absolute/path/to/.codex/skills/web-ui-smoke/scripts/runtime_info.sh`

## Fast preflight

1. Confirm the app URL responds with `curl`.
2. Confirm the shared smoke runtime under `$WEB_UI_SMOKE_RUNTIME_DIR` is actually usable.
3. If `playwright` import fails, or Chromium launch fails before the target page opens, stop the smoke loop and switch to `web-ui-doctor`.

## Workflow

1. Find how to run the app in the current repo.
2. Prefer an existing repo script from `package.json`, `Makefile`, or repo docs.
3. Start the app in a persistent shell session when possible.
4. Bind to `127.0.0.1` and use an explicit port when possible.
5. Wait until the page responds with `curl` before launching the browser.
6. Create an action plan inline or from a JSON file.
7. Run `$WEB_UI_CLIENT` against the target URL.
8. Review the saved screenshots and `summary.json`.
9. Fix the app or the steps and rerun.
10. Once the happy path works, keep one final screenshot artifact.
11. If you started a temporary local server for this run, stop it before the final answer unless the user explicitly asked to keep it running.

## Rules

- Prefer selectors over pixel clicks.
- Prefer `fill`, `click`, `press`, `waitForSelector`, `waitForText`, `assertText`, and `assertVisible`.
- Save artifacts inside the repo under `.codex-artifacts/web-ui/<run-id>/` unless the user asked otherwise.
- Always produce at least one final screenshot.
- Review `summary.json` for console, page, and request failures.
- If the repo already has a stable Playwright test suite, use that suite first and fall back to this skill only for ad hoc smoke flows.
- Keep the app server running while testing.
- Do not leave temporary local servers running after the smoke flow completes.
- If you launched `python3 -m http.server 4173 --bind 127.0.0.1` or a similar throwaway server, track how to stop it and terminate it before finishing.
- Prefer a repo stop script when available; otherwise stop the exact process or persistent session you started.
- Treat `.codex/skills/` as skill source only. Keep runtime dependencies under `$WEB_UI_SMOKE_RUNTIME_DIR`.
- Prefer the default runtime location under `$CODEX_HOME/runtimes/web-ui-smoke`. Override it only when isolation is intentional.
- Never patch the target repo or repo-root `node_modules` just to make the shared smoke runner import `playwright`.
- If `playwright` import or browser launch itself fails, stop guessing and switch to `web-ui-doctor`.

## Example command

```bash
RUN_DIR=".codex-artifacts/web-ui/$(date +%Y%m%dT%H%M%S)"
/absolute/path/to/.codex/skills/web-ui-smoke/scripts/run_smoke.sh \
  --url http://127.0.0.1:4173 \
  --actions-file "$WEB_UI_ACTIONS" \
  --screenshot-dir "$RUN_DIR" \
  --headless true
```

## Example inline actions

```json
{
  "steps": [
    { "op": "fill", "selector": "input[name='email']", "text": "test@example.com" },
    { "op": "fill", "selector": "input[name='password']", "text": "secret123" },
    { "op": "click", "selector": "button[type='submit']" },
    { "op": "waitForText", "selector": "body", "text": "Dashboard" },
    { "op": "screenshot", "name": "dashboard", "fullPage": true }
  ]
}
```

## Final answer format

- target URL
- runtime directory used
- app start command used
- action plan used
- artifacts directory
- screenshots created
- summary of visible result
- summary of console/page/request failures
- whether the temporary local server was stopped
- whether the flow passed fully or what failed first
