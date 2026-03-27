---
name: web-ui-doctor
description: "Use when browser testing is blocked and Codex must diagnose the exact failure layer: app server, local bind, reachability, repo wrapper, browser launch, trust/profile config, or sandbox/runtime. This is the doctor skill, not the normal runner."
argument-hint: "<url-or-prototype>"
user-invocable: true
---

# Playwright Run Doctor

Use this skill only when browser work is failing or flaky and you need to pinpoint the blocking layer.
Normal browser smoke testing should go through `web-ui-smoke`.

## Use when

- `web-ui-smoke` or a repo Playwright flow cannot open the page
- the page opens only with elevation or only outside the sandbox
- local server startup is unreliable
- you need to distinguish repo issues from Codex sandbox/runtime issues
- you need a crisp diagnosis instead of random retries

## Do not use for

- ordinary click/fill/screenshot tasks that already work
- writing or maintaining a full Playwright test suite
- iterating on canvas/game logic; use `develop-web-game`

## Read first if present in the repo

- `package.json`
- `.codex/config.toml`
- `docs/playwright-workflow.md`
- `scripts/playwright-cli-local.sh`
- `scripts/playwright-open-prototype.sh`
- `scripts/prototype-server.sh`
- `scripts/prototype-server-stop.sh`
- `references/repo-contract.md`

## Diagnosis order

1. Normalize the target.
   - Prefer an explicit URL.
   - If given a repo or prototype name, infer the local URL from repo scripts/docs.
2. Check whether the target port is already occupied.
   - If a stale repo server exists, stop it before blaming the sandbox.
3. Test local bind separately.
   - Prove whether a process can bind to `127.0.0.1:<port>`.
4. Test reachability separately.
   - Use `curl` against the target URL.
5. Test the Playwright runtime separately from the app.
   - First verify `playwright` import resolves from the intended shared runtime directory.
   - Then try a minimal page such as `data:text/html,<h1>ok</h1>`.
   - Then try the real target URL.
6. Compare launch modes.
   - Headless vs headed.
   - sandboxed vs the smallest justified elevated step.
7. Classify the failure and stop guessing.

## Failure classification

- **bind fails**
  - stale server already owns the port
  - local bind is restricted by current sandbox/runtime
  - repo trust or project config is not actually active
- **bind works, curl fails**
  - app server is not serving the expected page
  - wrong host/port/path
- **playwright import fails**
  - the shared smoke skill was not installed fully
  - the runtime is resolving from the wrong place
  - someone tried to lean on repo-local fallback resolution instead of fixing the real install
- **browser executable missing**
  - the Playwright package is present but browsers were not installed for that runtime
  - the runtime points at the wrong browser cache or revision
- **curl works, minimal browser launch fails**
  - browser launch is blocked by sandbox/runtime or browser install
- **minimal browser launch works, target URL fails**
  - app/runtime/content issue, not browser bootstrap
- **repo wrapper fails, direct skill-local browser launch works**
  - repo wrapper or repo environment is the problem
- **only headed fails**
  - GUI/display restrictions
- **only sandboxed launch fails, elevated launch works**
  - minimal working split proven; keep elevation only for launch

## Rules

- Use the smallest probe for each stage.
- Separate server, reachability, and browser launch. Do not collapse them into one giant command.
- Prefer the dedicated runtime directory at `$WEB_UI_SMOKE_RUNTIME_DIR` or `$CODEX_HOME/runtimes/web-ui-smoke`.
- For approval reuse, prefer the literal installed wrapper path and avoid `"$HOME/.codex/..."`, `"$CODEX_HOME/..."`, or `--runtime-dir` on ordinary home-runtime probes.
- Do not "fix" a missing shared Playwright runtime by adding shims or fallback `node_modules` to the target repo or `.codex/skills/`.
- Do not edit user-level Codex config unless the user explicitly asked for that.
- If an elevated step is required, escalate the exact failing command, not a vague description.
- Final answer must name the exact blocking layer.

## Minimal working split to aim for

1. local app server starts normally
2. `curl` confirms reachability
3. only browser launch is elevated if needed
4. follow-up snapshot/screenshots stay sandboxed if possible

## Return format

- target
- stages tested: bind, reachability, minimal launch, target launch, follow-up actions
- root cause
- exact blocking layer
- minimal working flow
- repo changes made, if any
- user-config changes only as proposed snippets
