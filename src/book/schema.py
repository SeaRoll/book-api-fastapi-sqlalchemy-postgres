from typing import Generic, TypeVar

from pydantic import BaseModel

from book import model

T = TypeVar("T")


class NewBookSchema(BaseModel):
    title: str
    description: str


class EditBookSchema(BaseModel):
    title: str
    description: str


class BookSchema(BaseModel):
    id: str
    title: str
    description: str

    @staticmethod
    def from_model(book: model.Book) -> "BookSchema":
        return BookSchema(
            id=book.id,
            title=book.title,
            description=book.description,
        )


class DataResponse(BaseModel, Generic[T]):
    data: list[T]


class SuccessResponse(BaseModel):
    success: bool
