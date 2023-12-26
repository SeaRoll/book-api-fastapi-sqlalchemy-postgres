from typing import Generic, TypeVar

from pydantic import BaseModel

from api import model

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


class MetadataResponse(BaseModel):
    """
    Metadata response for pagination

    Attributes
    ----------
    page : int
        The current page
    per_page : int
        The number of items per page
    total_pages : int
        The total number of pages
    total : int
        The total number of items
    """

    page: int
    per_page: int
    total_pages: int
    total: int


class PageResponse(BaseModel, Generic[T]):
    """
    Generic list data response with metadata

    Attributes
    ----------
    data : list[T]
        The data list
    metadata : MetadataResponse
        The metadata
    """

    data: list[T]
    metadata: MetadataResponse
