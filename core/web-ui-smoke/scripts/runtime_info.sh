#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

exec node "$SCRIPT_DIR/print_runtime_info.mjs" "$@"
