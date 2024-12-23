from rest_framework import routers


from . import views

router = routers.DefaultRouter()
router.register(r'payments', views.PaymentsViewSet)
app_name = "users"
urlpatterns = []
urlpatterns += router.urls

