# Generated by Django 3.2.5 on 2021-07-05 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('pub_date', models.DateField()),
                ('isbn_num', models.CharField(max_length=100)),
                ('page_count', models.IntegerField()),
                ('preview_link', models.URLField()),
                ('language', models.CharField(max_length=100)),
            ],
        ),
    ]
