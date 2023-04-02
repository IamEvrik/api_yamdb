"""Валидаторы."""

from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def valid_username_not_me(value):
    """Имя пользователя не может быть 'me'."""
    if value.lower() == 'me':
        raise ValidationError(
            _('Enter a valid username. This value can not be "me".')
        )


def valid_titles_year(value):
    """Год выпуска произведений не может быть больше текущего."""
    if value > datetime.today().year:
        raise ValidationError(
            _("Date can't be later than current year.")
        )
