import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import text

from api import config, database, migrator, schema
from api.app import app


class AppTest(unittest.TestCase):
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
        response = self.client.post(
            "/",
            json={
                "title": title,
                "description": description,
            },
        )
        return schema.BookSchema.model_validate(response.json())

    def test_get(self) -> None:
        created_book = self.create_book("foo", "bar")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        books = schema.DataResponse[schema.BookSchema].model_validate(response.json())
        self.assertEqual(len(books.data), 1)
        self.assertEqual(books.data[0].id, created_book.id)
        self.assertEqual(books.data[0].title, created_book.title)
        self.assertEqual(books.data[0].description, created_book.description)

    def test_post(self) -> None:
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
        response = self.client.put(
            "/random-id",
            json={
                "title": "foo2",
                "description": "bar2",
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_delete(self) -> None:
        created_book = self.create_book("foo", "bar")
        response = self.client.delete(f"/{created_book.id}")
        self.assertEqual(response.status_code, 200)

    def test_delete_400(self) -> None:
        response = self.client.delete("/random-id")
        self.assertEqual(response.status_code, 404)
