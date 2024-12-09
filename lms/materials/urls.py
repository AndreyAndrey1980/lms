from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'course', views.CourseViewSet)
app_name = "materials"
urlpatterns = [
    path("lesson/", views.LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", views.LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", views.LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/delete/", views.LessonDestroyApiView.as_view(), name="lesson_delete"),
    path("lesson/<int:pk>/update/", views.LessonUpdateApiView.as_view(), name="lesson_update")
]

urlpatterns += router.urls
