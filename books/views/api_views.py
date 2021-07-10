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

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        return render(request, self.template_name, {'form': form})

    def search(self, value, term):
        api_key = env('API_KEY')
        params = f'q=Hobbit+{term}:{value}&key={api_key}'
        books = requests.get(API_URL, params=params)
        books_json = books.json()
        return books_json['items']

    def add_books(self, books):
        for book in books:
            isbn = list(filter(
                lambda k: k['type'] != 'ISBN_10', book['volumeInfo'].get('industryIdentifiers'))
            )
            isbn13, = isbn

            author = book['volumeInfo'].get('authors')
            if author:
                author = author[0]

            p_date = book['volumeInfo'].get('publishedDate')

            if len(p_date) == 4:
                p_date += "-01-01"
            elif len(p_date) == 7:
                p_date += "-01"

            Book.objects.get_or_create(
                title=book['volumeInfo'].get('title'),
                author=author,
                pub_date=p_date,
                isbn_num=isbn13['identifier'],
                page_count=book['volumeInfo'].get('pageCount'),
                preview_link=book['volumeInfo'].get('previewLink'),
                language=book['volumeInfo'].get('language'),
            )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            term = request.POST['dropdown']
            books = self.search(keyword, term)
            self.add_books(books)

            return redirect('books:book_list')
