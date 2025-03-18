from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from . import views, stripe

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

router = routers.DefaultRouter()
router.register(r'payments', views.PaymentsViewSet, basename='payments')


urlpatterns = [
    path('register/', views.UsersCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),  # api/token
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('subscribe', views.SubscribeAPIView.as_view(), name='subscribe'),
    path('unsubscribe', views.UnsubscribeAPIView.as_view(), name='unsubscribe'),
    path('payments/create-payment/', views.PaymentsViewSet.as_view({'post': 'create_payment'}), name='create_payment'),
    path('stripe/success/', stripe.stripe_success, name='stripe-success'),
    path('stripe/cancel/', stripe.stripe_cancel, name='stripe-cancel'),
    path('stripe-webhook/', stripe.StripeWebhookAPIView.as_view(), name='stripe_webhook'),
    path('', include(router.urls)),
]
