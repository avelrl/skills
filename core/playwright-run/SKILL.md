---
name: playwright-run
description: "Run or diagnose a local Playwright prototype workflow: start a static server, open the page, capture snapshot or screenshot, and isolate whether failures come from repo config, trust, user config, or sandbox/runtime."
argument-hint: "<url-or-prototype>"
user-invocable: true
---

Purpose: Run or debug a repo-local Playwright browser flow with a sharp boundary between server reachability, browser launch, and follow-up inspection commands.

Use when:
- Codex needs to open a local prototype or app page via `playwright-cli` or a repo wrapper
- zero-manual browser flow is expected but fails in Codex
- the task requires proving whether the blocker is repo config, trusted-project state, user config, active profile, or host sandbox/runtime

Do not use for:
- general browser interaction tasks that do not need repo-local wrappers or sandbox diagnosis
- production E2E suites or Playwright test authoring
- editing the prototype/game itself; use `develop-web-game` for that

Inputs / Required Context:
- required: a target URL, prototype slug, or explicit local browser-run goal
- read first if present:
  - `docs/playwright-workflow.md`
  - `.codex/config.toml`
  - `scripts/playwright-cli-local.sh`
  - `scripts/playwright-open-prototype.sh`
  - `scripts/prototype-server.sh`
  - `scripts/prototype-server-stop.sh`
- if needed and permitted: inspect `~/.codex/config.toml` for trust and profile defaults
- read `references/repo-contract.md` when the repo needs scaffolding or standardization

Outputs / Owned Artifacts:
- owns no fixed project files by default
- may create transient run artifacts under `.playwright/` and `.playwright-cli/`
- may update repo-local scripts, docs, or `.codex/config.toml` only when the user wants to operationalize the flow
- must not edit user-level Codex config without explicit user request

Modes or Arguments:
- `<url-or-prototype>`: normalize into either an explicit URL or a repo-local prototype slug

Execution Rules:
1. Prefer repo-local wrappers and documented repo workflows over ad hoc commands.
2. Split diagnosis into ordered stages and test them separately:
   - local `bind()` / `listen()`
   - server reachability with `curl`
   - browser launch with `playwright-cli open`
   - follow-up `snapshot`
   - follow-up `screenshot`
3. Use the smallest direct probe for each stage before escalating to the full wrapper.
4. Treat trusted-project state as a first-class dependency. Project-scoped `.codex/config.toml` does not apply until the repo is trusted.
5. Before starting a new repo-local server, check whether the target port is already occupied by an existing repo process. If `scripts/prototype-server-stop.sh` exists, use it to clear stale repo-local servers that you started earlier.
6. If local bind fails after ruling out a stale or already-running local server, verify:
   - repo trust
   - repo `.codex/config.toml`
   - current approval/sandbox behavior
7. If server reachability works but `open` fails, capture the browser logs and classify the failure:
   - system-browser access to home-directory state such as Crashpad
   - generic sandboxed browser-launch abort
   - missing browser install
   - GUI/open-world restriction that needs escalation
8. If a required command fails because of sandboxing, request escalation with the exact wrapper command instead of asking in plain text first.
9. Do not assume `snapshot` and `screenshot` need the same privileges as `open`; once the browser session exists, retry them inside the normal sandbox.
10. Prefer repo-local runtime paths:
   - `PLAYWRIGHT_DAEMON_SESSION_DIR`
   - `PLAYWRIGHT_DAEMON_SOCKETS_DIR`
   - `PLAYWRIGHT_BROWSERS_PATH`
   - `NPM_CONFIG_CACHE`
11. When browser installation is needed, avoid global `~/.npm` or global Playwright browser caches if they are blocked; use repo-local paths and the repo-pinned Playwright package where possible.
12. Distinguish two successful outcomes:
   - full sandboxed flow works end to end
   - minimal working split works: unsandboxed `open`, sandboxed `snapshot` and `screenshot`
13. If you start a temporary server during diagnosis, stop it before finishing unless the user asked to keep it running.
14. Final answer must name the exact blocking layer:
   - repo config
   - user config
   - trust or active profile
   - host sandbox or runtime

Failure / Stop Conditions:
- stop if no target URL or prototype can be inferred
- stop if the user forbids escalation and browser launch remains sandbox-blocked
- record the exact failing command and error instead of generalizing

Return Format:
- target
- stages tested: `bind`, `reachability`, `open`, `snapshot`, `screenshot`
- root cause
- exact blocking layer
- minimal working flow
- repo changes made, if any
- user-config diff only as a proposed snippet, never as an unrequested edit

Example Invocation:
- `/playwright-run is-basic-melee-commitment-readable-under-pressure`
- `/playwright-run http://127.0.0.1:4173/prototypes/foo/index.html`

Related Skills / Boundary:
- use `playwright` for direct terminal browser commands and page interaction once the environment is already healthy
- use `develop-web-game` when the task is to iterate on the game or prototype itself, not merely run and diagnose it
