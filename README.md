# Books API

A simple Crud API example on FastAPI, Pyscopg3 and SQLAlchemy

## Features

- Create, Read, Update and Delete books
- Simple migrator for database
- Simple test for API

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
pip install "psycopg[binary,pool]" # For psycopg3
pip install -r requirements.txt
```

## Run Fully Locally

```sh
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
python -m unittest discover src
docker compose -f docker-compose.test.yml down
```
