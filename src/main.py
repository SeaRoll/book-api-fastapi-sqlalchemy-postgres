import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI

import database
import migrator
import model
import schema

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Starting up")
    migrator.run_migration(Path("./migrations"), database.SessionLocal, 1)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def get() -> schema.DataResponse[schema.BookSchema]:
    with database.SessionLocal() as session:
        books = (
            session.query(model.Book)
            .where(model.Book.is_deleted == False)
            .all()
        )
        books = [schema.BookSchema.from_model(book) for book in books]
        return schema.DataResponse(data=books)


@app.post("/", status_code=201)
def post(newBook: schema.NewBookSchema) -> schema.SuccessResponse:
    with database.SessionLocal() as session:
        with session.begin():
            book = model.Book.new(newBook.title, newBook.description)
            session.add(book)
            session.commit()
    return schema.SuccessResponse(success=True)


@app.put("/{id}")
def put(id: str, editBook: schema.EditBookSchema) -> schema.SuccessResponse:
    with database.SessionLocal() as session:
        with session.begin():
            book = session.get(model.Book, id)
            book.title = editBook.title
            book.description = editBook.description
            session.merge(book)
            session.commit()
    return schema.SuccessResponse(success=True)


@app.delete("/{id}")
def delete(id: str) -> schema.SuccessResponse:
    with database.SessionLocal() as session:
        with session.begin():
            book = session.get(model.Book, id)
            book.is_deleted = True
            session.merge(book)
            session.commit()
    return schema.SuccessResponse(success=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
