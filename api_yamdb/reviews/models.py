"""
Модели для приложения reviews.
"""

from typing import Tuple

from django.core.validators import RegexValidator
from typing_extensions import Final

from django.contrib.auth.models import AbstractUser
from django.db import models


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

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=9,
        choices=_USER_ROLES_CHOICES,
        default=USER,
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
    )


class Categories(models.Model):
    """Модель жанры"""

    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Slug doesnt comply',
            ),
        ]
    )

    def __str__(self):
        return self.name
