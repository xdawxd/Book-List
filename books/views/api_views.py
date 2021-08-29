from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from books.api.serializers import BookSerializer
from django.views.generic import View, ListView, FormView
from django.shortcuts import redirect
from django.core import serializers
from books.models import Book
from books.forms import SearchBookForm, ImportConfirmForm
from django.http import JsonResponse
from django.shortcuts import render
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

    def set_session_data(self, request, data):
        for key, value in data.items():
            request.session[key] = value
        request.session.modified = True

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        data = {
            'book_name': request.POST.get('book_name'),
            'keyword': request.POST.get('keyword'),
            'term': request.POST.get('dropdown')
        }

        self.set_session_data(request, data)

        # return redirect('books:api_import_confirm')


class ImportConfirmView(ListView):
    form_class = ImportConfirmForm
    template_name = 'books/import_modal.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_name = None
        self.keyword = None
        self.term = None
        self.book_list = []

    def get_context_data(self, **kwargs):
        kwargs['modal_form'] = kwargs.pop('form')
        return super(ImportConfirmView, self).get_context_data(**kwargs)

    def set_session_data(self, request, books):
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
            self.book_list.append(book)

    def add_books(self, books):
        for book in books:
            book.save()

    def is_already_added(self, books, isbn):
        books += Book.objects.all()
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
                if book.isbn_num == isbn and action == 'added' and not self.is_already_added(checked_books, isbn):
                    checked_books.append(book)
        return checked_books

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        self.book_name = request.session.get('book_name')
        self.keyword = request.session.get('keyword')
        self.term = request.session.get('term')

        books_json = self.search(self.book_name, self.keyword, self.term)
        self.get_books(books_json)

        self.set_session_data(request, self.book_list)

        context = {
            'book_name': self.book_name,
            'keyword': self.keyword,
            'term': self.term,
            'books': self.book_list,
            'form': form,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return

        data = json.loads(request.body)
        books = request.session.get('books')

        checked_books = self.get_checked_books(data, books)
        self.add_books(checked_books)

        return JsonResponse('Books imported.', safe=False)
