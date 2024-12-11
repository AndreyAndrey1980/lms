from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'payments', views.PaymentsViewSet)
app_name = "users"
urlpatterns = []
urlpatterns += router.urls