# Project Overview

This project is a web application that allows users to manage their drinks consumed every day. It is built using Python, Flask, and Bootstrap framework. It uses PostgreSQL for data storage and SQLite in local.

## Architecture

- **Pattern**: Factory pattern with `create_app()` in `app.py`
- **Blueprints**: `auth`, `main`, `api_routes`, `swagger_ui`
- **Flow**: Models → Controllers (static methods) → Routes/Blueprints
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Auth**: Flask-Login with session-based authentication
- **Config**: Pydantic BaseSettings (Development / Testing / Production)

## Folder Structure

- `/falken_drinks`: Contains the source code for the Python backend.
- `/templates`: Contains the HTML templates for the Flask application.
- `/static`: Contains static files for the Flask application, including CSS and JavaScript.
- `/tests`: Contains test cases for the application.
- `/falken_drinks.db`: SQLite database file for local development.
- `.env`: Environment variables for the application.
- `pyproject.toml`: Project config and dependencies.
- `app.yaml`: Configuration file for deploying the application on Google App Engine.

## Libraries and Frameworks

- Flask and Bootstrap for the frontend.
- Flask for the backend.
- PostgreSQL for data storage (SQLite in dev/test).
- SQLAlchemy for ORM (Object Relational Mapping).
- Pydantic for settings management.
- Flask-Login for authentication.
- Jest for JavaScript testing.

## Coding Standards

- Use a consistent naming convention for files and directories (e.g., lowercase with underscores).
- Use single quotes for strings.
- Follow PEP 8 guidelines for Python code style.
- Max line length: 127 characters (flake8 config).
- Max cyclomatic complexity: 10.
- Write clear and concise comments to explain the purpose of code blocks.
- Use meaningful variable and function names to enhance code readability.
- Use the project's logging module: `from falken_drinks.logger import Log`.
- Timestamps in CET timezone using `now_cet()` from config.

## Testing

- **Python**: pytest + unittest, inherit from `BaseTestCase` in `tests/basetest.py`
- **JavaScript**: Jest with jsdom environment
- **Run all**: `./check_app.sh` (Python) + `npm test` (JS)
- **Coverage**: `coverage run -m pytest -v -s`

## UI guidelines

- A toggle is provided to switch between light and dark mode.
- Application should have a modern and clean design.
- Use Bootstrap components to ensure responsiveness and consistency across different devices.

## Resources

For detailed instructions, see:
- **Agents**: `.github/agents/` (test-writer, code-reviewer, feature-developer, debugger)
- **Prompts**: `.github/prompts/` (python, tests, templates, models, code-review)
- **Instructions**: `.github/instructions/` (coding-standards, testing, security)
- **Copilot config**: `.github/copilot/` (config, snippets)