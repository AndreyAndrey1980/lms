from .serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from .models import Lesson, Course
from users.permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, )
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner)

        return super().get_permissions()


class LessionViewSet(viewsets.ModelViewSet):
    """CRUD для уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModerator, IsOwner)

        return super().get_permissions()
