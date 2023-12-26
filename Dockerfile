FROM python:3.11-alpine

COPY ./pyproject.toml ./pyproject.toml
COPY ./.env.production ./.env
COPY ./src ./src
COPY ./migrations ./migrations

RUN pip install "psycopg[binary,pool]"
RUN pip install -e .

CMD ["python", "-m", "src.main"]
