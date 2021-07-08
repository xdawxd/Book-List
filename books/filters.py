import django_filters
from django_filters import DateFilter
from books.models import Book
from django import forms


class BookFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        label='Title',
        lookup_expr='icontains',
        widget=forms.widgets.TextInput(attrs={'class': 'search-bar'})
    )
    author = django_filters.CharFilter(
        label='Author',
        lookup_expr='icontains',
        widget=forms.widgets.TextInput(attrs={'class': 'search-bar'})
    )
    language = django_filters.CharFilter(
        label='Language',
        lookup_expr='exact',
        widget=forms.widgets.TextInput(attrs={'class': 'search-bar'})
    )
    pub_min = DateFilter(
        label='Date From',
        field_name='pub_date',
        lookup_expr='gte',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'search-bar',
        })
    )
    pub_max = DateFilter(
        label='To',
        field_name='pub_date',
        lookup_expr='lte',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'search-bar',
        })
    )

    class Meta:
        model = Book
        fields = ()
