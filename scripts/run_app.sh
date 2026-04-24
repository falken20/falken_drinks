#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="${ROOT_DIR}/.venv/bin/activate"

if [[ -f "${VENV_PATH}" ]]; then
	# Reuse the local virtualenv when available.
	source "${VENV_PATH}"
fi

export FLASK_APP="falken_drinks.app:create_app"
export FLASK_ENV="${FLASK_ENV:-development}"

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-5000}"

cd "${ROOT_DIR}"

echo "Starting Falken Drinks on http://${HOST}:${PORT}"

exec flask run --host "${HOST}" --port "${PORT}"