# Generated by Django 3.2 on 2023-04-01 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_titles_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ('id',), 'verbose_name': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'ordering': ('id',), 'verbose_name': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='titles',
            options={'ordering': ('id',), 'verbose_name': 'Произведения'},
        ),
    ]
