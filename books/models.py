from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
# Create your models here.


class Book(models.Model):
    title = models.CharField('Title', max_length=100, validators=[MinLengthValidator(2)])
    author = models.CharField('Author', max_length=100, validators=[MinLengthValidator(2)])
    pub_date = models.DateField('Publication Date')
    isbn_num = models.CharField('ISBN', max_length=100)
    page_count = models.IntegerField('Number of Pages', validators=[MinValueValidator(1)])
    preview_link = models.URLField('Preview')
    language = models.CharField('Language', max_length=100, validators=[MinLengthValidator(2)])

    def __str__(self):
        return self.title
