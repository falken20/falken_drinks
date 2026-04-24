#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

if [ -x ".venv/bin/coverage" ]; then
	COVERAGE_BIN=".venv/bin/coverage"
else
	COVERAGE_BIN="coverage"
fi

# Unit test and coverage
echo "***** Run Tests *****"
"$COVERAGE_BIN" run -m pytest -q # -v -s
test_status=$?
# coverage run -m pytest -v -s # Version with more output for debugging

#### Probar un solo test: pytest -v -s tests/test_auth.py::TestAuth::test_auth_login
echo "***** Coverage tests last execution *****"
coverage_output=$("$COVERAGE_BIN" report --omit="*/tests/*,*/venv/*" -m ./falken_drinks/*.py)
printf "%s\n" "$coverage_output"

# Keep README coverage badge in sync with the latest Python suite execution.
coverage_pct=$(printf "%s\n" "$coverage_output" | awk '/TOTAL/{gsub("%", "", $NF); print $NF; exit}')
if [ "$test_status" -eq 0 ] && [ -n "$coverage_pct" ] && [ -f "README.md" ]; then
	encoded_pct="${coverage_pct}%25"
	today=$(date +%Y-%m-%d)
	tmp_file=$(mktemp)
	awk -v encoded_pct="$encoded_pct" -v today="$today" '
	{
		gsub(/https:\/\/img\.shields\.io\/badge\/coverage-[0-9]+%25-green/, "https://img.shields.io/badge/coverage-" encoded_pct "-green")
		gsub(/Last verified: `[0-9]{4}-[0-9]{2}-[0-9]{2}`\./, "Last verified: `" today "`.")
		print
	}' README.md > "$tmp_file" && mv "$tmp_file" README.md
	echo "***** README coverage badge updated to ${coverage_pct}% (Last verified: ${today}) *****"
else
	echo "***** README coverage badge not updated (tests failed or coverage missing) *****"
fi

# Coverage report in html
# coverage run -m pytest -v && coverage html --omit="*/test/*,*/venv/*"

# With param -s for input
# coverage run -m pytest -v -s && coverage html --omit="*/test/*,*/venv/*"

# Linter checks
# stop the build if there are Python syntax errors or undefined names
echo "***** Linter: Checking Python syntax errors *****"
flake8 ./falken_drinks/* --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
echo "***** Linter: Checking Python syntax patterns *****"
flake8 ./falken_drinks/* --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics