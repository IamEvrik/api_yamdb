import csv
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (User, Categories, Genres, Titles, GenreTitle)
from api_yamdb.settings import BASE_DIR

CSV_DIRS = BASE_DIR / 'static/data'

CATEGORIES_FILE = r'\category.csv'
GENRES_FILE = r'\genre.csv'
TITLES_FILE = r'\titles.csv'
USERS_FILE = r'\users.csv'
GENRE_TITLE_FILE = r'\genre_title.csv'

class Command(BaseCommand):
    def handle(self, *args, **options):
        if Categories.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    'Отмена импорта. '
                    'Таблица с категориями уже содержит данные.'))
            pass
        else:
            try:
                bulk_list = []
                with open(f'{CSV_DIRS}{CATEGORIES_FILE}',
                          encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        print(row)
                        category = Categories(
                            pk=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                        bulk_list.append(category)
                    Categories.objects.bulk_create(bulk_list)
            except Exception as error:
                raise CommandError(error)
            self.stdout.write(
                self.style.SUCCESS('Категории импортированы успешно'))

        if Genres.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    'Отмена импорта. '
                    'Таблица с жанрами уже содержит данные.'))
            pass
        else:
            try:
                bulk_list = []
                with open(f'{CSV_DIRS}{GENRES_FILE}',
                          encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        print(row)
                        genre = Genres(
                            pk=row['id'],
                            name=row['name'],
                            slug=row['slug'],
                        )
                        bulk_list.append(genre)
                    Genres.objects.bulk_create(bulk_list)
            except Exception as error:
                raise CommandError(error)
            self.stdout.write(
                self.style.SUCCESS('Жанры импортированы успешно'))

        if Titles.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    'Отмена импорта. '
                    'Таблица с произведениями уже содержит данные.'))
            pass
        else:
            try:
                bulk_list = []
                with open(f'{CSV_DIRS}{TITLES_FILE}',
                          encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        print(row)
                        title = Titles(
                            pk=row['id'],
                            name=row['name'],
                            year=row['year'],
                            category_id=row['category']
                        )
                        bulk_list.append(title)
                    Titles.objects.bulk_create(bulk_list)
            except Exception as error:
                raise CommandError(error)
            self.stdout.write(
                self.style.SUCCESS('Произведения импортированы успешно'))

        if User.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    'Отмена импорта. '
                    'Таблица с пользователями уже содержит данные.'))
            pass
        else:
            try:
                bulk_list = []
                with open(f'{CSV_DIRS}{USERS_FILE}',
                          encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        print(row)
                        user = User(
                            pk=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name']
                        )
                        bulk_list.append(user)
                    User.objects.bulk_create(bulk_list)
            except Exception as error:
                raise CommandError(error)
            self.stdout.write(
                self.style.SUCCESS('Пользователи импортированы успешно'))

        if GenreTitle.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    'Отмена импорта. '
                    'Таблица с жанры-произведения уже содержит данные.'))
            pass
        else:
            try:
                bulk_list = []
                with open(f'{CSV_DIRS}{GENRE_TITLE_FILE}',
                          encoding="utf-8-sig") as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        print(row)
                        genre_title = GenreTitle(
                            pk=row['id'],
                            title_id=row['title_id'],
                            genre_id=row['genre_id']
                        )
                        bulk_list.append(genre_title)
                    GenreTitle.objects.bulk_create(bulk_list)
            except Exception as error:
                raise CommandError(error)
            self.stdout.write(
                self.style.SUCCESS('Жанры-произведения импортированы успешно'))