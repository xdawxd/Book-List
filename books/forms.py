from django import forms
from books.models import Book


class BookForm(forms.ModelForm):
    isbn_num = forms.CharField(
        label="ISBN:",
        widget=forms.widgets.TextInput(attrs={
            'class': 'form-control form-input'}
        )
    )

    pub_date = forms.DateField(
        label='Publication Date',
        widget=forms.widgets.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-input'}
        )
    )

    def clean_language(self):
        lang = self.cleaned_data['language']
        if lang:
            if any(n.isdigit() for n in lang):
                raise forms.ValidationError('This field cannot contain numbers.')

            return lang

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'author': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'page_count': forms.NumberInput(attrs={'class': 'form-control form-input'}),
            'preview_link': forms.TextInput(attrs={'class': 'form-control form-input'}),
            'language': forms.TextInput(attrs={'class': 'form-control form-input'}),
        }


class SearchBookForm(forms.Form):
    book_name = forms.CharField(
        label='Name', widget=forms.widgets.TextInput(attrs={'class': 'form-control form-input'}))
    keyword = forms.CharField(
        label='Keyword', widget=forms.widgets.TextInput(attrs={'class': 'form-control form-input'}))


class ImportConfirmForm(forms.Form):
    check_box = forms.BooleanField(
        required=False,
        label="Import?",
        widget=forms.CheckboxInput(attrs={
            'onchange': 'checkbox.ifChecked(this);',
            'class': 'form-check-input',
        }))
