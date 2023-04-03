"""Загрузка информации из csv файлов."""

import csv
import pathlib

from django.conf import settings
from django.core.management import base

from reviews.models import (Categories, Comment, Genres, Review, Title,
                            TitleGenre, User)


class Command(base.BaseCommand):
    """Загрузка модели из csv-файла."""

    FILES_CLASS_MAPPING = {
        'users.csv': User,
        'category.csv': Categories,
        'genre.csv': Genres,
        'titles.csv': Title,
        'genre_title.csv': TitleGenre,
        'review.csv': Review,
        'comments.csv': Comment,
    }

    DATA_DIR = settings.STATICFILES_DIRS[0] / 'data'

    def handle(self, *args, **options):
        """Загрузка."""
        for filename in Command.FILES_CLASS_MAPPING:
            full_name = Command.DATA_DIR / filename
            if full_name.exists():
                cur_class = Command.FILES_CLASS_MAPPING[filename]
                with open(full_name, 'r', encoding='utf8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=',')
                    for row in reader:
                        cur_class.objects.get_or_create(**row)
                    self.stdout.write(f'file {filename} processed\n')
