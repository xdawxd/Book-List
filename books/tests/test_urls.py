from django.urls import reverse, resolve


class TestUrls:

    def test_book_list_url(self):
        path = reverse('books:book_list')
        assert resolve(path).view_name == 'books:book_list'

    def test_book_detail_url(self):
        path = reverse('books:book_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'books:book_detail'

    def test_book_create_url(self):
        path = reverse('books:book_new')
        assert resolve(path).view_name == 'books:book_new'

    def test_book_update_url(self):
        path = reverse('books:book_update', kwargs={'pk': 1})
        assert resolve(path).view_name == 'books:book_update'

    def test_book_delete_url(self):
        path = reverse('books:book_delete', kwargs={'pk': 1})
        assert resolve(path).view_name == 'books:book_delete'
