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
