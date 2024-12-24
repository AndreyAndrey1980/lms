from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Course, Lesson


class OwnerOrModeratorPermission(BasePermission):
    """
    Доступ авторизованным пользователям
    Модераторы не могут создавать или удалять объекты.
    """
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'DELETE':
            return not request.user.groups.filter(name='Moderators')
        return request.user.is_authenticated or request.user.groups.filter(name='Moderators')

