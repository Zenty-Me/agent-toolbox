#!/usr/bin/env bash
# Compatibility entry point; Python is also directly usable on Windows.
set -euo pipefail
exec python3 "$(dirname "$0")/sync_skills.py" "$@"
