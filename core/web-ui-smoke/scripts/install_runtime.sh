#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
RUNTIME_DIR="${WEB_UI_SMOKE_RUNTIME_DIR:-$CODEX_HOME/runtimes/web-ui-smoke}"
PLAYWRIGHT_SPEC="$(node -p "const pkg = require(process.argv[1]); pkg.dependencies.playwright;" "$SKILL_DIR/package.json")"

mkdir -p "$RUNTIME_DIR"

npm install \
  --prefix "$RUNTIME_DIR" \
  --no-save \
  --package-lock=false \
  "playwright@$PLAYWRIGHT_SPEC"

PLAYWRIGHT_BROWSERS_PATH="$RUNTIME_DIR/browsers" \
PLAYWRIGHT_SKIP_BROWSER_GC=1 \
  "$RUNTIME_DIR/node_modules/.bin/playwright" install chromium

printf 'web-ui-smoke runtime ready: %s\n' "$RUNTIME_DIR"
printf 'playwright package: %s\n' "$RUNTIME_DIR/node_modules/playwright"
printf 'browser cache: %s\n' "$RUNTIME_DIR/browsers"
