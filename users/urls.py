from django.urls import path, include
from rest_framework import routers

from . import views

app_name = "users"

router = routers.DefaultRouter()
router.register(r'payments', views.PaymentsViewSet, basename='payments')
router.register('', views.UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]