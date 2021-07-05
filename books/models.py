from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pub_date = models.DateField()
    isbn_num = models.CharField(max_length=100)
    page_count = models.IntegerField()
    preview_link = models.URLField()
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.title
