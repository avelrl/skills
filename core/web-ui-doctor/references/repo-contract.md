# Repo Contract

Use this file when a repo needs a repeatable local browser-run flow.
This is for repo shaping, not for the global reusable runner itself.

## Minimal repo shape

Preferred files:

- `scripts/prototype-server.sh`
- `scripts/prototype-server-stop.sh`
- `docs/playwright-workflow.md`
- optional: `scripts/playwright-cli-local.sh`
- optional: `.codex/config.toml`

## Server baseline

Prefer a small explicit wrapper that binds to localhost and prints the final URL.

Example:

```bash
#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-4173}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory app
```

## Stop script baseline

```bash
#!/usr/bin/env bash
set -euo pipefail
PORT="${1:-4173}"
if command -v lsof >/dev/null 2>&1; then
  PIDS="$(lsof -ti tcp:"$PORT" || true)"
  if [ -n "$PIDS" ]; then
    kill $PIDS
  fi
fi
```

Temporary local servers used only for smoke or doctor probes should be stopped after the run.
Do not leave `python3 -m http.server 4173 --bind 127.0.0.1` or similar throwaway servers alive once artifacts are captured.

## Project Codex config baseline

Project-scoped `.codex/config.toml` should stay small and explicit.
It only matters after the repo is trusted.

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

## Direct probes

Bind test:

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
curl -sfI http://127.0.0.1:4173/
```

Skill-runtime import check:

```bash
/absolute/path/to/.codex/skills/web-ui-smoke/scripts/runtime_info.sh
```

For approval reuse, prefer the literal installed wrapper path.
Do not spell the command as `"$HOME/.codex/..."`, `"$CODEX_HOME/..."`, or similar shell-expanded variants when the home-level install path is already known.

Minimal browser launch check:

```bash
/absolute/path/to/.codex/skills/web-ui-smoke/scripts/run_smoke.sh \
  --url 'data:text/html,<h1>ok</h1>' \
  --actions-json '{"steps":[{"op":"waitForText","selector":"body","text":"ok","contains":true},{"op":"screenshot","name":"ok"}]}' \
  --screenshot-dir .codex-artifacts/web-ui-doctor
```

Do not add `--runtime-dir` for the ordinary default home-runtime path.
Reserve it for explicit runtime override or diagnosis comparisons.

If the runtime package probe fails, install the runtime with:

```bash
/absolute/path/to/.codex/skills/web-ui-smoke/scripts/install_runtime.sh
```

If the launch check still fails after that, the problem is the shared Playwright runtime, not the app repo.
If the data URL works but the app URL does not, the browser bootstrap is probably fine.
