from rest_framework import permissions

from .models import Course, Lesson

class OwnerOrModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'destroy':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Moderators').exists():
            return view.action not in ['create', 'destroy']
        if isinstance(obj, Course):
            return obj.owner == request.user
        if isinstance(obj, Lesson):
            return obj.owner == request.user
        return False
