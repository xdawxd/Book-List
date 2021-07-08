from django import forms
from books.models import Book
from django.core.validators import MinValueValidator, MinLengthValidator


class BookForm(forms.ModelForm):
    pub_date = forms.DateField(label='Publication Date', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    isbn_num = forms.CharField(label="ISBN:")

    def clean_isbn_num(self):
        isbn = self.cleaned_data['isbn_num']
        if len(isbn) != 13:
            raise forms.ValidationError('This number should be 13 digits long.')

        return isbn

    def clean_language(self):
        lang = self.cleaned_data['language']
        if any(n.isdigit() for n in lang):
            raise forms.ValidationError('This field cannot contain numbers.')

        return lang

    class Meta:
        model = Book
        fields = '__all__'

