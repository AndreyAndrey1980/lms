from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

router = routers.DefaultRouter()
router.register(r'payments', views.PaymentsViewSet, basename='payments')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UsersCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),  # api/token
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('subscribe', views.SubscribeAPIView.as_view(), name='subscribe'),
    path('unsubscribe', views.UnsubscribeAPIView.as_view(), name='unsubscribe'),gi
    path('create-product/', views.CreateProductAPIView.as_view(), name='create_product'),
    path('create-payment-intent/', views.CreatePaymentIntentAPIView.as_view(), name='create_payment_intent'),
    path('stripe-webhook/', views.StripeWebhookAPIView.as_view(), name='stripe_webhook'),
]
