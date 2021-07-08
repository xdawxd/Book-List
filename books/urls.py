from django.urls import path
from books import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book_new'),
    path('book/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/remove/', views.BookDeleteView.as_view(), name='book_delete'),
    # path('book/search_for/', views.SearchListView.as_view(), name='search_list'),
]
