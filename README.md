# Books API

A simple Crud API example on FastAPI, Pyscopg3 and SQLAlchemy

## Features

- Create, Read, Update and Delete books
- Simple migrator for database
- Simple test for API & Coverage (Even on GitHub Actions)
- Type checking with MyPy
- Linting with Ruff

## Requirements

- Python 3.11
- Docker
- A `.env` file with the following variables

```sh
# .env
DATABASE_URL=...
```

## Installation

```sh
python -m venv .venv
source .venv/bin/activate
pip install 'psycopg[binary,pool]' # For psycopg3
pip install -e .
pip install -e '.[dev]'
```

#### Usage with VSCode

For VSCode, extensions `Python`, `Mypy Type Checker`, and `Ruff` are recommended.

Then in the `settings.json`, put these configurations:

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    },
    "editor.formatOnSave": true
  },
  "mypy-type-checker.path": ["./.venv/bin/mypy"],
  "mypy-type-checker.interpreter": ["./.venv/bin/python"],
  "mypy-type-checker.args": ["--config-file", "./pyproject.toml"],
  "ruff.format.args": ["--config=./pyproject.toml"]
}
```

## Run Fully Locally

```sh
#1. Create a `.env.production` file
#2. Run the following command:
docker compose up
```

## Testing

#### Environment Variables

```sh
# .env
DATABASE_URL=postgresql+psycopg://postgres:mysecretpassword@localhost:5432/postgres
```

#### Run tests

```sh
docker compose -f docker-compose.test.yml up -d
coverage run -m unittest discover src
docker compose -f docker-compose.test.yml down
```
