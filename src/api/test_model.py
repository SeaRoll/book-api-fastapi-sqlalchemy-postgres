import unittest

from api.model import Book


class BookModelTest(unittest.TestCase):
    def test_new_book(self) -> None:
        title = "A book title"
        description = "A book description"
        book = Book.new(title, description)
        self.assertEqual(book.title, title)
        self.assertEqual(book.description, description)
