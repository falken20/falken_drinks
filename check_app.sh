#!/bin/sh

# Compatibility wrapper: keep historical command working.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/scripts/check_app.sh" "$@"
