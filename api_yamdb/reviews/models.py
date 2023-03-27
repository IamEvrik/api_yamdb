"""
Модели для приложения reviews.
"""

from typing import Tuple

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
