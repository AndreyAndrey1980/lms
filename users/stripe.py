import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from materials.models import Course, Lesson
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.models import Payments

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_product(name):
    """Создает объект продукта"""
    product = stripe.Product.create(name=name)
    return product


def create_price(price, name):
    """Создает объект цены"""
    product_id = create_product(name).id
    response = stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product=product_id
    )
    return response


def create_session(price, name):
    """Создает сессию в Stripe и возвращает ID и URL сессии"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/courses/",
        line_items=[{"price": create_price(price, name), "quantity": 1}],
        mode="payment",
    )
    return session


def stripe_success(request):
    return JsonResponse({"message": "Payment successful! Redirecting..."})


def stripe_cancel(request):
    return JsonResponse({"message": "Payment canceled. Try again."})

