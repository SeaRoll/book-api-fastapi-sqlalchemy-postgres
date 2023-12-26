import unittest

from api.model import Book


class BookModelTest(unittest.TestCase):
    """
    Test to check the Book model transformation
    """

    def test_new_book(self) -> None:
        """
        Given   A title and a description
        When    A new book is created
        Then    It should have the same title and description
                And the id should not be None
        """

        title = "A book title"
        description = "A book description"
        book = Book.new(title, description)
        self.assertIsNotNone(book.id)
        self.assertEqual(book.title, title)
        self.assertEqual(book.description, description)
