# Generated by Django 3.2.5 on 2021-07-08 21:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn_num',
            field=models.CharField(max_length=100, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='page_count',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Number of Pages'),
        ),
        migrations.AlterField(
            model_name='book',
            name='preview_link',
            field=models.URLField(verbose_name='Preview'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pub_date',
            field=models.DateField(verbose_name='Publication Date'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
