"""Модели для приложения reviews."""

from typing import Tuple

from typing_extensions import Final

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.validators import valid_username_not_me


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
        return self.role == User.ADMIN

    @property
    def is_moderator(self) -> bool:
        """Является ли пользователь модератором."""
        return self.role == User.MODERATOR
