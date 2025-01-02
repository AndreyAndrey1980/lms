from django.urls import path
from . import views
from rest_framework import routers
from django.urls import path, include

app_name = "materials"

router = routers.DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='courses')
router.register(r'lesson', views.LessionViewSet, basename='lessons')

urlpatterns = [path('', include(router.urls))]
