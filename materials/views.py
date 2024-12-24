from .serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from .models import Lesson, Course
from .permissions import OwnerOrModeratorPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import  PermissionDenied

PERMISSION_CLASSES = [IsAuthenticated, OwnerOrModeratorPermission]


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = PERMISSION_CLASSES

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied('Вы не можете удалить чужой контент.')
        return super().perform_destroy(instance)


class LessionViewSet(viewsets.ModelViewSet):
    """CRUD для уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = PERMISSION_CLASSES
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied('Вы не можете удалить чужой контент.')
        return super().perform_destroy(instance)
