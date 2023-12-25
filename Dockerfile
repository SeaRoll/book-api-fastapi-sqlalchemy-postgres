FROM python:3.11-alpine

COPY ./requirements.txt ./requirements.txt
RUN pip install "psycopg[binary,pool]"
RUN pip install -r requirements.txt

COPY ./.env.production ./.env
COPY ./src ./src
COPY ./migrations ./migrations

CMD ["python", "./src/main.py"]
