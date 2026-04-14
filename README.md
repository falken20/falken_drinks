<div align="center">
<img src="./static/images/logo_app.png" alt="Falken Drinks logo" width="320"/>

# Falken Drinks

Track your daily drinks, review your hydration habits, and manage your drink catalog from a Flask web app.

<p>
	<img src="https://img.shields.io/github/languages/count/falken20/falken_drinks" alt="GitHub language count"/>&nbsp;
	<img src="https://img.shields.io/github/languages/top/falken20/falken_drinks" alt="GitHub top language"/>&nbsp;
	<img src="https://img.shields.io/github/license/falken20/falken_drinks" alt="GitHub license"/>&nbsp;
	<img src="https://img.shields.io/static/v1?label=python&message=3.11%2B&color=blue&logo=python&logoColor=white" alt="Python version"/>&nbsp;
	<img src="https://img.shields.io/badge/release-0.1.0-blue" alt="Release version"/>&nbsp;
	<img src="https://img.shields.io/badge/ci-passing-brightgreen" alt="CI status"/>&nbsp;
	<img src="https://img.shields.io/badge/coverage-90%25-green" alt="Test coverage"/>
</p>

<p>
	<a href="https://richionline-portfolio.nw.r.appspot.com">
		<img src="https://img.shields.io/badge/web-richionline-blue" alt="Portfolio"/>
	</a>
	<a href="https://twitter.com/richionline">
		<img src="https://img.shields.io/twitter/follow/richionline?style=social" alt="Twitter"/>
	</a>
</p>
</div>

## Overview

Falken Drinks is a Flask application focused on daily drink tracking. It combines a classic server-rendered web interface with API endpoints, authentication, analytics views, and Swagger documentation.

The project is designed with a clean backend structure based on:

- Flask application factory
- SQLAlchemy models
- Controllers for business logic
- Blueprints for route separation
- SQLite for local development and tests
- PostgreSQL for production

## Features

- User authentication with Flask-Login
- Daily drink logging
- Drink catalog management
- Analytics and summary views
- Swagger UI for API exploration
- Responsive UI built with Bootstrap
- Light and dark mode support
- Python and JavaScript automated tests

## Tech Stack

- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login
- Frontend: Jinja2 templates, Bootstrap, Vanilla JavaScript
- Database: SQLite in local/testing, PostgreSQL in production
- Config: Pydantic Settings + `.env`
- Testing: `pytest`, `unittest`, `coverage`, `Jest`, `jsdom`
- Deployment: Google App Engine + Gunicorn

## Quick Start

### 1. Prerequisites

- Python `3.11+`
- Node.js `20+`
- `npm`

### 2. Clone and enter the project

```bash
git clone https://github.com/falken20/falken_drinks.git
cd falken_drinks
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install --upgrade pip
pip install -e ".[dev,lint]"
```

### 5. Install JavaScript test dependencies

```bash
npm install
```

### 6. Configure environment variables

```bash
cp .env.sample .env
```

Then edit `.env` with the values you need.

### 7. Run the application

```bash
flask --app falken_drinks.app:create_app run
```

Open the app at `http://127.0.0.1:5000/`.

## Environment Configuration

The project reads configuration from `.env` and maps it through Pydantic settings.

Core variables from `.env.sample`:

```bash
LEVEL_LOG="DEBUG, INFO, WARNING, ERROR"
CONFIG_MODE="development"
DEVELOPMENT_DATABASE_URL="sqlite://database.db"
TESTING_DATABASE_URL="sqlite:///:memory:"
PRODUCTION_DATABASE_URL=
SECRET_KEY=
```

Configuration modes:

- `development`
- `testing`
- `production`

## Run Tests And Quality Checks

### Python tests + coverage + linting

```bash
./check_app.sh
```

This script runs:

- `pytest` with coverage
- Coverage report for `falken_drinks/*.py`
- `flake8` syntax checks
- `flake8` style checks

Coverage note: the `87%` badge in the header is verified from the current Python suite (`coverage run -m pytest -q`).
Last verified: `2026-04-14`.

### Run only Python tests

```bash
coverage run -m pytest -v -s
coverage report --omit="*/tests/*,*/venv/*" -m ./falken_drinks/*.py
```

### Run one specific test

```bash
pytest -v -s tests/test_auth.py::TestAuth::test_auth_login
```

### JavaScript tests

```bash
npm test
```

### JavaScript coverage

```bash
npm run test:coverage
```

## Swagger API Docs

Once the application is running, Swagger UI is available at:

```text
http://127.0.0.1:5000/swagger/
```

## Project Structure

```text
falken_drinks/
├── falken_drinks/
│   ├── app.py          # Flask app factory
│   ├── auth.py         # Auth blueprint
│   ├── main.py         # Main views blueprint
│   ├── routes.py       # API blueprint
│   ├── controllers.py  # Business logic
│   ├── models.py       # SQLAlchemy models
│   ├── config.py       # Environment and settings
│   ├── logger.py       # Logging utilities
│   ├── cache.py        # Cache checks/helpers
│   └── swagger.py      # Swagger configuration
├── templates/          # Jinja2 templates
├── static/             # CSS, JS and images
├── tests/              # Python and JS tests
├── .github/            # CI, templates, prompts, agents, instructions
├── pyproject.toml      # Python project metadata and dependencies
├── package.json        # Jest configuration for frontend tests
├── check_app.sh        # Python checks entrypoint
└── app.yaml            # Google App Engine deployment config
```

## Architecture

The backend follows a simple and maintainable flow:

```text
Models -> Controllers -> Blueprints / Routes -> Templates or JSON responses
```

Main architectural points:

- `create_app()` factory in `falken_drinks/app.py`
- Blueprints: `auth`, `main`, `api_routes`, `swagger_ui`
- SQLAlchemy models with serialization helpers
- Controller classes with static methods
- Flask-Login session-based authentication
- Timezone-aware helpers in CET

## Deployment

Production deployment is prepared for Google App Engine.

Main details from `app.yaml`:

- Runtime: `python310`
- Entrypoint: `gunicorn -b:$PORT 'falken_drinks.app:create_app()'`
- Static handler for `/static`
- Production settings via environment variables and `credentials.yaml`

Deploy command:

```bash
gcloud app deploy app.yaml
```

## Development Notes

- Local and test environments use SQLite
- Production uses PostgreSQL
- Logging is managed through `falken_drinks.logger.Log`
- Coding style uses single quotes and a max line length of `127`
- JavaScript tests live under `tests/js/`

## GitHub Automation And AI Helpers

The repository includes reusable GitHub and Copilot resources under `.github/`:

- Workflows for CI and deploy
- Issue templates and PR template
- Reusable prompts for Python, tests, templates and models
- Project-specific instructions for coding, testing and security
- AI agents for code review, feature development, debugging and test writing

## Roadmap Ideas

- Improve analytics and reporting views
- Add stronger form validation and UX feedback
- Expand test coverage further
- Add migration workflow for schema evolution

## License

This project is licensed under the MIT License. See `LICENSE` for details.
