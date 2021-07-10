from books.models import Book
from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestModels:

    def test_book_create(self):
        book = mixer.blend(Book, quantity=1)
        latest_book = Book.objects.last()
        assert latest_book.title == book.title
