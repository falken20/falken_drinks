#!/bin/sh

# Unit test and coverage
echo "***** Run Tests *****"
coverage run -m pytest -v -s
# coverage run -m unittest -v
#### Probar un solo test: pytest -v -s tests/test_auth.py::TestAuth::test_auth_login
echo "***** Coverage tests last execution *****"
coverage report --omit="*/tests/*,*/venv/*" -m ./falken_plants/*.py 

# Coverage report in html
# coverage run -m pytest -v && coverage html --omit="*/test/*,*/venv/*"

# With param -s for input
# coverage run -m pytest -v -s && coverage html --omit="*/test/*,*/venv/*"

# Linter checks
# stop the build if there are Python syntax errors or undefined names
echo "***** Linter: Checking Python syntax errors *****"
flake8 ./falken_plants/* --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
echo "***** Linter: Checking Python syntax patterns *****"
flake8 ./falken_plants/* --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics