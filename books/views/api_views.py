from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from books.api.serializers import BookSerializer
from django.views.generic import View, ListView
from django.core import serializers
from books.models import Book
from books.forms import SearchBookForm, ImportConfirmForm
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from . import API_URL
import pandas as pd
from myproject.settings import env


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        'title': ['icontains'],
        'author': ['icontains'],
        'language': ['icontains'],
        'pub_date': ['gte', 'lte'],
    }


class ImportBookView(View):
    form_class = SearchBookForm
    template_name = 'books/book_import.html'

    def set_search_session_data(self, request, data):
        for key, value in data.items():
            request.session[key] = value
        request.session.modified = True

    def set_book_session_data(self, request, books):
        request.session['books'] = serializers.serialize('json', books)

    def correct_date(self, pub_date):
        return pd.to_datetime(pub_date)

    def correct_isbn(self, book):
        return list(filter(
            lambda k: k['type'] != 'ISBN_10', book['volumeInfo'].get('industryIdentifiers'))
        )

    def search(self, name, value, term):
        api_key = env('API_KEY')
        params = f'q={name}+{term}:{value}&key={api_key}'  # TODO -> rewrite this hardcoded url
        books = requests.get(API_URL, params=params)
        books_json = books.json()
        return books_json.get('items')

    def get_books(self, books_json):  # TODO -> add try and except for weird book names
        book_list = []
        for book in books_json:
            pub_date = self.correct_date(book['volumeInfo'].get('publishedDate'))
            author = book['volumeInfo'].get('authors')[-1]  # TODO -> add author model and fix this
            isbn, = self.correct_isbn(book)

            book = Book(
                title=book['volumeInfo'].get('title'),
                author=author,
                pub_date=pub_date,
                isbn_num=isbn['identifier'],
                page_count=book['volumeInfo'].get('pageCount'),
                preview_link=book['volumeInfo'].get('previewLink'),
                language=book['volumeInfo'].get('language')
            )
            book_list.append(book)
        return book_list

    def add_books(self, books):
        for book in books:
            book.save()

    def is_already_created(self, isbn):
        try:
            created_books = Book.objects.values_list('isbn_num')[0]
        except IndexError:
            return False

        if isbn in created_books:
            return True
        return False

    def is_already_added(self, books, isbn):
        for book in books:
            if book.isbn_num == isbn:
                return True
        return False

    def get_checked_books(self, data, books):
        checked_books = []
        for isbn, action in data.items():
            for book in json.loads(books):
                book['fields']['pub_date'] = self.correct_date(book['fields']['pub_date'])
                book = Book(**book['fields'])
                if book.isbn_num == isbn \
                        and action == 'added' \
                        and not self.is_already_added(checked_books, isbn) \
                        and not self.is_already_created(isbn):
                    checked_books.append(book)
        return checked_books

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        checkbox = ImportConfirmForm(request.GET)
        return render(request, self.template_name, {'form': form, 'checkbox': checkbox})

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        if 'searchSubmit' == data.get('submitBtn'):
            book_name = data.get('book_name')
            keyword = data.get('keyword')
            term = data.get('dropdown')

            books_json = self.search(book_name, keyword, term)
            book_list = self.get_books(books_json)

            self.set_book_session_data(request, book_list)

            response = serializers.serialize('json', book_list)
            return JsonResponse(response, safe=False)

        else:
            data = json.loads(request.body)
            book_list = request.session.get('books')

            checked_books = self.get_checked_books(data, book_list)
            self.add_books(checked_books)
            return JsonResponse('OK', safe=False)  # add redirecting
