from django.urls import reverse_lazy
from books.models import Book
from books.forms import BookForm
from books.filters import BookFilter
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView)


# Create your views here.


class BookListView(ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        return context


class BookDetailView(DetailView):
    model = Book


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book_list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('books:book_list')


class BookDeleteView(DeleteView):
    fields = '__all__'
    model = Book
    success_url = reverse_lazy('books:book_list')
