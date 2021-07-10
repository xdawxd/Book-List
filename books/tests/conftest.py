from books.views.api_views import ImportBookView
import pytest


@pytest.fixture
def view():
    return ImportBookView()
