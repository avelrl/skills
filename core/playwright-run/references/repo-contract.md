# Repo Contract

Use this file only when the repo needs a repeatable local Playwright run flow or when the current repo is missing the standard wrappers.

## Minimal Repo Shape

Preferred files:

- `scripts/playwright-cli-local.sh`
- `scripts/playwright-open-prototype.sh`
- `scripts/prototype-server.sh`
- `scripts/prototype-server-stop.sh`
- `docs/playwright-workflow.md`
- `.codex/config.toml`

## Wrapper Baseline

`scripts/playwright-cli-local.sh` should prefer repo-local runtime paths:

```bash
export PLAYWRIGHT_DAEMON_SESSION_DIR="${PLAYWRIGHT_DAEMON_SESSION_DIR:-$ROOT_DIR/.playwright/daemon-sessions}"
export PLAYWRIGHT_DAEMON_SOCKETS_DIR="${PLAYWRIGHT_DAEMON_SOCKETS_DIR:-$ROOT_DIR/.playwright/daemon-sockets}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$ROOT_DIR/.playwright/browsers}"
mkdir -p "$PLAYWRIGHT_DAEMON_SESSION_DIR" "$PLAYWRIGHT_DAEMON_SOCKETS_DIR" "$PLAYWRIGHT_BROWSERS_PATH"
```

This avoids daemon-state writes outside the workspace and keeps browser downloads portable with the repo if needed.

## Static Server Baseline

Minimal server wrapper:

```bash
python3 -m http.server "$PORT" --bind 127.0.0.1
```

Avoid `0.0.0.0` unless the repo explicitly needs it.

## Project Codex Config Baseline

Project-scoped `.codex/config.toml` should be minimal and explicit:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"
default_permissions = "playwright_local"

[sandbox_workspace_write]
network_access = true

[permissions.playwright_local.filesystem]
":project_roots" = { "." = "write" }
"/tmp" = "write"

[permissions.playwright_local.network]
enabled = true
mode = "limited"
allowed_domains = ["localhost", "127.0.0.1"]
allow_local_binding = true
```

Important: this file matters only after the repo is trusted.

## Direct Probe Commands

Use the smallest probes first.

Local bind:

```bash
python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 4173))
print("bind-ok")
s.close()
PY
```

Reachability:

```bash
curl -sfI http://127.0.0.1:4173/path/to/page
```

Browser open:

```bash
./scripts/playwright-cli-local.sh -s=prototype open http://127.0.0.1:4173/path/to/page --headed
```

Follow-up:

```bash
./scripts/playwright-cli-local.sh -s=prototype snapshot
./scripts/playwright-cli-local.sh -s=prototype screenshot
```

## Repo-Local Browser Install

If browser installation is needed, prefer repo-local cache paths and the Playwright version already pinned by the repo:

```bash
mkdir -p .playwright/npm-cache
if [ ! -x ./node_modules/.bin/playwright ]; then
  echo "Install repo dependencies first so browser install matches the repo-pinned Playwright version." >&2
  exit 1
fi
NPM_CONFIG_CACHE="$PWD/.playwright/npm-cache" \
PLAYWRIGHT_BROWSERS_PATH="$PWD/.playwright/browsers" \
./node_modules/.bin/playwright install firefox
```

Do not rely on a floating `npx playwright ...` install or on `playwright-cli install-browser` unless they are known to match that repo and environment.

## Interpretation Matrix

- `bind()` fails before browser launch:
  - target port is already occupied by an old server or another local process
  - clean up the stale process before blaming repo config
  - repo trust not applied yet
  - repo `.codex/config.toml` not loaded or ineffective
  - host sandbox is still tighter than repo config can relax

- server works, `open` fails with Chrome Crashpad or home-directory file access:
  - browser launch is blocked by filesystem sandbox around the system browser

- repo-local Firefox or another Playwright-managed browser also aborts:
  - restriction is broader than Chrome profile state; it is a sandboxed browser-launch problem

- unsandboxed `open` succeeds and sandboxed `snapshot` or `screenshot` succeed:
  - minimal working split is proven
  - keep `open` as the only elevated step

- `snapshot` and `screenshot` fail even after a successful unsandboxed `open`:
  - session artifacts or daemon sockets are not repo-local enough, or the session name/path is inconsistent
