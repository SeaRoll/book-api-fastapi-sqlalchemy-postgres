import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import uvicorn
from api import config, database, migrator, model, schema
from fastapi import FastAPI, HTTPException

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> Any:
    migrator.run_migration(
        Path(str(config.cfg.get("MIGRATION_PATH"))),
        database.SessionLocal,
        int(config.cfg.get("MIGRATION_VERSION")),
    )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def get() -> schema.DataResponse[schema.BookSchema]:
    with database.SessionLocal() as session:
        books = session.query(model.Book).where(model.Book.is_deleted == False).all()
        books_schema = [schema.BookSchema.from_model(book) for book in books]
        return schema.DataResponse(data=books_schema)


@app.post("/", status_code=201)
def post(newBook: schema.NewBookSchema) -> schema.BookSchema:
    with database.SessionLocal() as session:
        with session.begin():
            book = model.Book.new(newBook.title, newBook.description)
            session.add(book)
            session.commit()
            return schema.BookSchema.from_model(book)


@app.put("/{id}")
def put(id: str, editBook: schema.EditBookSchema) -> schema.BookSchema:
    with database.SessionLocal() as session:
        with session.begin():
            book = session.get(model.Book, id)
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            book.title = editBook.title
            book.description = editBook.description
            session.merge(book)
            session.commit()
            return schema.BookSchema.from_model(book)


@app.delete("/{id}")
def delete(id: str) -> schema.SuccessResponse:
    with database.SessionLocal() as session:
        with session.begin():
            book = session.get(model.Book, id)
            if book is None or book.is_deleted:
                raise HTTPException(status_code=404, detail="Book not found")
            book.is_deleted = True
            session.merge(book)
            session.commit()
    return schema.SuccessResponse(success=True)


def run() -> None:
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
