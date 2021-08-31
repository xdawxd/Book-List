from django.urls import path
from books.views import book_views, api_views

app_name = 'books'

urlpatterns = [
    path('', book_views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>', book_views.BookDetailView.as_view(), name='book_detail'),
    path('book/new/', book_views.BookCreateView.as_view(), name='book_new'),
    path('book/<int:pk>/edit/', book_views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/remove/', book_views.BookDeleteView.as_view(), name='book_delete'),
    path('api/book-list/', api_views.BookList.as_view(), name='api_book_list'),
    path('api/import-book/', api_views.ImportBookView.as_view(), name='api_book_import'),
]
