import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import text

from book import database, migrator, schema
from book.app import app


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        migrator.run_migration(Path("./migrations"), database.SessionLocal, 1)

    def setUp(self) -> None:
        self.client = TestClient(app)
        with database.SessionLocal() as session:
            with session.begin():
                session.execute(text("DELETE FROM books"))
                session.commit()

    def create_book(self, title: str, description: str) -> None:
        self.client.post(
            "/",
            json={
                "title": title,
                "description": description,
            },
        )

    def test_get(self) -> None:
        self.create_book("foo", "bar")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        books = schema.DataResponse[schema.BookSchema].model_validate(
            response.json()
        )
        self.assertEqual(len(books.data), 1)
        self.assertEqual(books.data[0].title, "foo")
        self.assertEqual(books.data[0].description, "bar")

    def test_post(self) -> None:
        response = self.client.post(
            "/",
            json={
                "title": "foo",
                "description": "bar",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"success": True})
