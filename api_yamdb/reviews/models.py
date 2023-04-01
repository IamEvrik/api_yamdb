"""Модели для приложения reviews."""

from typing import Tuple

from typing_extensions import Final

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.validators import valid_username_not_me


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

    class Meta:
        verbose_name = _('Category')


class Genres(BaseModelGenreCategorie):
    """Модель жанры."""

    class Meta:
        verbose_name = _('Genre')
