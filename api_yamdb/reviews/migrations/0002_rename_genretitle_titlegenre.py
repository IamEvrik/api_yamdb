# Generated by Django 3.2 on 2023-04-03 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GenreTitle',
            new_name='TitleGenre',
        ),
    ]