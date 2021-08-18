from django.test.client import Client
from django.urls import reverse
import pytest
from mixer.backend.django import mixer
from pytest_django.asserts import assertTemplateUsed, assertContains, assertRedirects
from books.models import Book


@pytest.mark.django_db
class TestViews:

    def test_book_list_view(self):
        client = Client()
        response = client.get(reverse('books:book_list'))

        assert response.status_code == 200
        assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        book = mixer.blend(Book, quantity=1)
        client = Client()
        response = client.get(reverse('books:book_detail', kwargs={'pk': book.id}))

        assert response.status_code == 200
        assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_create_view(self):
        client = Client()
        book = mixer.blend(Book, quantity=1)

        # response = client.get(reverse('books:book_new'))
        # assert response.status_code == 200

        post_response = client.post(
            reverse('books:book_new'),
            {
                'title': book.title,
                'author': book.author,
                'pub_date': book.pub_date,
                'isbn_num': '9782123456803',
                'page_count': 123,
                'language': book.language,
                'preview_link': book.preview_link,

            },
            follow=True)
        assertRedirects(post_response, reverse('books:book_list'), status_code=302)

        latest_book = Book.objects.last()
        assert latest_book.author == book.author

    def test_book_update_view(self):
        client = Client()
        book = mixer.blend(Book, quantity=1)
        response = client.post(
            reverse('books:book_update', kwargs={'pk': book.id}),
            {
                'title': book.title,
                'author': book.author,
                'pub_date': book.pub_date,
                'isbn_num': '9782123456803',  # updated values
                'page_count': 123,
                'language': book.language,
                'preview_link': book.preview_link,
            }
        )

        assertRedirects(response, reverse('books:book_list'), status_code=302)

    def test_book_delete_view(self):
        client = Client()
        book = mixer.blend(Book, quantity=1)

        response = client.get(reverse('books:book_delete', kwargs={'pk': book.id}), follow=True)
        assertContains(response, 'Are you sure you want to delete')

        post_response = client.post(reverse('books:book_delete', kwargs={'pk': book.id}), follow=True)
        assertRedirects(post_response, reverse('books:book_list'), status_code=302)
