from materials.serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from materials.models import Lesson, Course
from users.permissions import IsModerator, IsOwner
from materials.celery import send_course_update_email, check_and_send_lesson_update
from rest_framework.permissions import IsAuthenticated
from materials.paginators import MyPagination
import datetime


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_at = datetime.datetime.now()
        instance.save()
        
        response = super().update(request, *args, **kwargs)

        send_course_update_email.delay(instance.id)

        return response

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsModerator)
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
    pagination_class = MyPagination

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        course = instance.course
        last_course_update_time = course.updated_at

        instance.updated_at = datetime.datetime.now()
        instance.save()

        response = super().update(request, *args, **kwargs)

        check_and_send_lesson_update.delay(course.id, last_course_update_time)

        return response
