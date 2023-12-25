import uuid

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    @staticmethod
    def new(title: str, description: str) -> "Book":
        return Book(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            is_deleted=False,
        )
