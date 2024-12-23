from .serializers import LessonSerializer, CourseSerializer
from rest_framework import viewsets
from .models import Lesson, Course
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from .permissions import OwnerOrModeratorPermission
from rest_framework.permissions import IsAuthenticated

PERMISSION_CLASSES = [IsAuthenticated, OwnerOrModeratorPermission]


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = PERMISSION_CLASSES


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = PERMISSION_CLASSES

class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = PERMISSION_CLASSES


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = PERMISSION_CLASSES

class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = PERMISSION_CLASSES

class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = PERMISSION_CLASSES