
class TestViews:

    def test_book_search(self, view):
        assert view.search('The Hobbit', 'intitle')[1] == 200
