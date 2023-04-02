"""Разрешения для приложения."""

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешения только для пользователей с ролью администратора."""

    def has_permission(self, request, view):
        """Проверка доступа к списку."""
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешения всем на чтение, на редактирование только админу."""

    def has_permission(self, request, view):
        """Проверка прав на доступ к списку и на создание."""
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        """Проверка прав на доступ к объекту."""
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_admin
        )
