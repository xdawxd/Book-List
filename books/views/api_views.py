from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from books.api.serializers import BookSerializer
from django.views.generic import View
from django.shortcuts import redirect
from books.models import Book
from books.forms import SearchBookForm
from django.shortcuts import render
import requests
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

    def correct_date(self, pub_date):
        return str(pd.to_datetime(pub_date)).split(' ')[0]

    def correct_isbn(self, book):
        return list(filter(
            lambda k: k['type'] != 'ISBN_10', book['volumeInfo'].get('industryIdentifiers'))
        )

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def search(self, name, value, term):
        api_key = env('API_KEY')
        params = f'q={name}+{term}:{value}&key={api_key}'  # TODO -> rewrite this hardcoded url
        books = requests.get(API_URL, params=params)
        print(books.url)
        books_json = books.json()
        return books_json['items']

    def add_books(self, books):
        for book in books:
            pub_date = self.correct_date(book['volumeInfo'].get('publishedDate'))
            author = book['volumeInfo'].get('authors')[-1]  # TODO -> add author model and fix this
            isbn, = self.correct_isbn(book)

            Book.objects.get_or_create(
                title=book['volumeInfo'].get('title'),
                author=author,
                pub_date=pub_date,
                isbn_num=isbn['identifier'],
                page_count=book['volumeInfo'].get('pageCount'),
                preview_link=book['volumeInfo'].get('previewLink'),
                language=book['volumeInfo'].get('language'),
            )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return

        book_name = form.cleaned_data['book_name']
        keyword = form.cleaned_data['keyword']
        term = request.POST['dropdown']
        books = self.search(book_name, keyword, term)
        self.add_books(books)

        return redirect('books:book_list')
