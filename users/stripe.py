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


def create_or_fetch_stripe_product(subject: Course | Lesson, amount: int,
        user, subject_type):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    stripe_product = None
    stripe_price = None

    existing_products = stripe.Product.list(limit=100) 
    for product in existing_products['data']:
        if product['name'] == subject.name:
            stripe_product = product
            break

    if stripe_product:
        existing_prices = stripe.Price.list(product=stripe_product.id, active=True)
        for price in existing_prices['data']:
            if price['unit_amount'] == amount:
                stripe_price = price
                break

    if not stripe_product:
        stripe_product = stripe.Product.create(
            name=subject.name,
            description=subject.description,
            images=[subject.preview] if subject.preview else []
        )

    if not stripe_price:
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=amount,
            currency='usd'
        )
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': stripe_price.id,
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://localhost:8000/stripe/success/",
        cancel_url="http://localhost:8000/stripe/cancel/",
        metadata={
            'user_id': user.id,
            'subject': subject_type,
            'course_id': subject.id if subject_type == Payments.SubjectType.COURSE else '',
            'lesson_id': subject.id if subject_type == Payments.SubjectType.LESSON else '',
        }
    )

    return session


def stripe_success(request):
    return JsonResponse({"message": "Payment successful! Redirecting..."})


def stripe_cancel(request):
    return JsonResponse({"message": "Payment canceled. Try again."})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        payload = request.body
        signature_header = request.headers.get("Stripe-Signature")
        if not signature_header:
            return JsonResponse({"error": "Missing Stripe-Signature header"}, status=400)

        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload=request.body,
                sig_header=signature_header,
                secret=webhook_secret
            )
            print("Webhook received:", event["type"])

        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            print("Invalid signature:", str(e))
            return JsonResponse({"error": "Invalid signature"}, status=400)

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']

        return Response({'status': 'success'}, status=201)