from typing import Generic, TypeVar

from api import model
from pydantic import BaseModel

T = TypeVar("T")


class NewBookSchema(BaseModel):
    """
    Schema for creating a new book

    Attributes
    ----------
    title : str
        The book title
    description : str
        The book description
    """

    title: str
    description: str


class EditBookSchema(BaseModel):
    """
    Schema for editing a book

    Attributes
    ----------
    title : str
        The book title
    description : str
        The book description
    """

    title: str
    description: str


class BookSchema(BaseModel):
    """
    The book schema

    Attributes
    ----------
    id : str
        The book id
    title : str
        The book title
    description : str
        The book description
    """

    id: str
    title: str
    description: str

    @staticmethod
    def from_model(book: model.Book) -> "BookSchema":
        """
        Creates a new book schema from a book model

        Parameters
        ----------
        book : Book
            The book model

        Returns
        -------
        BookSchema
            The created book schema
        """

        return BookSchema(
            id=book.id,
            title=book.title,
            description=book.description,
        )


class DataResponse(BaseModel, Generic[T]):
    """
    A generic list data response

    Attributes
    ----------
    data : list[T]
        The data list
    """

    data: list[T]


class SuccessResponse(BaseModel):
    """
    A success response

    Attributes
    ----------
    success : bool
        Whether the operation was successful or not
    """

    success: bool
