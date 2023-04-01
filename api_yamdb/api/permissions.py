"""Разрешения для приложения."""

from rest_framework import permissions


class UserIsAdmin(permissions.BasePermission):
    """Разрешения только для пользователей с ролью администратора."""

    def has_permission(self, request, view):
        """Проверка доступа к списку."""
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
