"""
Модели для приложения reviews.
"""

from typing import Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES_CHOICES: Tuple[Tuple[str, str], ...] = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Переопределение встроенного класса User."""

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=9,
        choices=USER_ROLES_CHOICES,
        default='user',
    )
