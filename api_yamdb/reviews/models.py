"""Модели для приложения reviews."""

from typing import Tuple
from typing_extensions import Final
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.validators import valid_titles_year, valid_username_not_me


class BaseModelGenreCategorie(models.Model):
    """Базовая модель для жанров и категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Slug doesnt comply',
            ),
        ],
        verbose_name='slug'
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('id',)


class User(AbstractUser):
    """Переопределение встроенного класса User."""

    USER: Final[str] = 'user'
    ADMIN: Final[str] = 'admin'
    MODERATOR: Final[str] = 'moderator'
    _USER_ROLES_CHOICES: Tuple[Tuple[str, str], ...] = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=(
            valid_username_not_me,
            AbstractUser.username_validator
        )
    )
    bio = models.TextField(
        _('bio'),
        blank=True,
    )
    role = models.CharField(
        _('role'),
        max_length=9,
        choices=_USER_ROLES_CHOICES,
        default=USER,
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
    )
    password = models.CharField(_('password'), max_length=128, blank=True)

    class Meta:
        ordering = ('pk',)

    @property
    def is_admin(self) -> bool:
        """Является ли пользователь администратором."""
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self) -> bool:
        """Является ли пользователь модератором."""
        return self.role == User.MODERATOR


class Categories(BaseModelGenreCategorie):
    """Модель категории."""

    class Meta(BaseModelGenreCategorie.Meta):
        verbose_name = 'Категории'


class Genres(BaseModelGenreCategorie):
    """Модель жанры."""

    class Meta(BaseModelGenreCategorie.Meta):
        verbose_name = 'Жанры'


class Titles(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=(valid_titles_year,)
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Slug жанра'
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Slug категории',
        on_delete=models.DO_NOTHING
    )

    class Meta(BaseModelGenreCategorie.Meta):
        verbose_name = 'Произведения'
        default_related_name = 'titles'
        
        
 class Review(models.Model):
    """Отзывы."""
    
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1')
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name='reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text[:15]
