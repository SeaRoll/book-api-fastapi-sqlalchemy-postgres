import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException

from api import config, database, migrator, model, schema

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> Any:
    """
    A lifespan event handler to run the migration before the app starts

    Parameters
    ----------
    _ : FastAPI
        The FastAPI instance

    Yields
    ------
    Any
        The yielded value
    """
    migrator.run_migration(
        Path(str(config.cfg.get("MIGRATION_PATH"))),
        database.SessionLocal,
        int(config.cfg.get("MIGRATION_VERSION")),
    )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def get() -> schema.DataResponse[schema.BookSchema]:
    """
    Returns the list of books

    Returns
    -------
    schema.DataResponse[schema.BookSchema]
        The list of books
    """

    with database.SessionLocal() as session:
        books = session.query(model.Book).where(model.Book.is_deleted == False).all()
        books_schema = [schema.BookSchema.from_model(book) for book in books]
        return schema.DataResponse(data=books_schema)


@app.post("/", status_code=201)
def post(new_book: schema.NewBookSchema) -> schema.BookSchema:
    """
    Creates a new book

    Parameters
    ----------
    new_book : schema.NewBookSchema
        The new book data

    Returns
    -------
    schema.BookSchema
        The created book
    """

    with database.SessionLocal() as session:
        with session.begin():
            book = model.Book.new(new_book.title, new_book.description)
            session.add(book)
            session.commit()
            return schema.BookSchema.from_model(book)


@app.put("/{id}")
def put(id: str, edit_book: schema.EditBookSchema) -> schema.BookSchema:
    """
    Updates a book with the given id

    Parameters
    ----------
    id : str
        The book id
    edit_book schema.EditBookSchema
        The book data

    Raises
    ------
    HTTPException
        If the book is not found

    Returns
    -------
    schema.BookSchema
        The updated book
    """
    with database.SessionLocal() as session:
        with session.begin():
            book = session.get(model.Book, id)
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            book.title = edit_book.title
            book.description = edit_book.description
            session.merge(book)
            session.commit()
            return schema.BookSchema.from_model(book)


@app.delete("/{id}")
def delete(id: str) -> schema.SuccessResponse:
    """
    Deletes a book with the given id

    Parameters
    ----------
    id : str
        The book id

    Raises
    ------
    HTTPException
        If the book is not found

    Returns
    -------
    schema.SuccessResponse
        The success response
    """
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
