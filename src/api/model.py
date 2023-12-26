import uuid

from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base


class Book(Base):
    """
    The book model

    Attributes
    ----------
    id : str
        The book id
    title : str
        The book title
    description : str
        The book description
    is_deleted : bool
        Whether the book is deleted or not
    """

    __tablename__ = "books"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    @staticmethod
    def new(title: str, description: str) -> "Book":
        """
        Creates a new book instance with generated id

        Parameters
        ----------
        title : str
            The book title
        description : str
            The book description

        Returns
        -------
        Book
            The created book instance
        """
        return Book(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            is_deleted=False,
        )
