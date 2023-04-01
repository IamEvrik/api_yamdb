"""Разрешения для приложения."""

from rest_framework import permissions


class UserIsAdmin(permissions.BasePermission):
    """Разрешения только для пользователей с ролью администратора."""

    def has_permission(self, request, view):
        """Проверка доступа к списку."""
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
                    request.user.is_authenticated and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
