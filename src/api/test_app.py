import unittest
from pathlib import Path

from api import config, database, migrator, schema
from api.app import app
from fastapi.testclient import TestClient
from sqlalchemy import text


class AppTest(unittest.TestCase):
    """
    Test to check the API endpoints
    """

    @classmethod
    def setUpClass(cls) -> None:
        migrator.run_migration(
            Path(str(config.cfg.get("MIGRATION_PATH"))),
            database.SessionLocal,
        )

    def setUp(self) -> None:
        self.client = TestClient(app)
        with database.SessionLocal() as session:
            with session.begin():
                session.execute(text("DELETE FROM books"))
                session.commit()

    def create_book(self, title: str, description: str) -> schema.BookSchema:
        """
        Creates a book using the API

        Parameters
        ----------
        title : str
            The book title
        description : str
            The book description

        Returns
        -------
        schema.BookSchema
            The created book
        """

        response = self.client.post(
            "/",
            json={
                "title": title,
                "description": description,
            },
        )
        return schema.BookSchema.model_validate(response.json())

    def test_get(self) -> None:
        """
        Given   A book is created
        When    The books list is requested
        Then    It should return the created book within the list
        """

        created_book = self.create_book("foo", "bar")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        books = schema.DataResponse[schema.BookSchema].model_validate(response.json())
        self.assertEqual(len(books.data), 1)
        self.assertEqual(books.data[0].id, created_book.id)
        self.assertEqual(books.data[0].title, created_book.title)
        self.assertEqual(books.data[0].description, created_book.description)

    def test_post(self) -> None:
        """
        When    A new book is created
        Then    It should return the created book
                And the id should not be None
        """
        response = self.client.post(
            "/",
            json={
                "title": "foo",
                "description": "bar",
            },
        )
        self.assertEqual(response.status_code, 201)
        book = schema.BookSchema.model_validate(response.json())
        self.assertIsNotNone(book.id)
        self.assertEqual(book.title, "foo")
        self.assertEqual(book.description, "bar")

    def test_put(self) -> None:
        """
        Given   A book is created
        When    The book is updated
        Then    It should return the updated book
                And the id should not be None
                And the returned book should have the updated values
        """

        created_book = self.create_book("foo", "bar")
        response = self.client.put(
            f"/{created_book.id}",
            json={
                "title": "foo2",
                "description": "bar2",
            },
        )
        self.assertEqual(response.status_code, 200)
        book = schema.BookSchema.model_validate(response.json())
        self.assertEqual(book.id, created_book.id)
        self.assertEqual(book.title, "foo2")
        self.assertEqual(book.description, "bar2")

    def test_put_400(self) -> None:
        """
        Given   A book does not exist
        When    A book is updated
        Then    It should return a 404
        """

        response = self.client.put(
            "/random-id",
            json={
                "title": "foo2",
                "description": "bar2",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_delete(self) -> None:
        """
        Given   A book is created
        When    The book is deleted
        Then    It should return a 200
        """

        created_book = self.create_book("foo", "bar")
        response = self.client.delete(f"/{created_book.id}")
        self.assertEqual(response.status_code, 200)

    def test_delete_400(self) -> None:
        """
        Given   A book does not exist
        When    A book is deleted
        Then    It should return a 404
        """

        response = self.client.delete("/random-id")
        self.assertEqual(response.status_code, 404)
