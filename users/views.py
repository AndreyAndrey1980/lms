import datetime
import stripe
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render
from rest_framework import viewsets
from .models import Payments, User, Subscription
from .serializers import PaymentsSerializer, UserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from materials.models import Course
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['pay_method', 'lesson', 'course']
    ordering_fields = ['date']
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, pay_method=Payments.PayMethod.TRANSFER, lesson=None,
                        date=datetime.datetime.now(), subject=Payments.SubjectType.COURSE)

class UsersCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        course_id = request.data["course_id"]
        course_item = Course.objects.get(pk=course_id)
        try:
            subs_item = Subscription.objects.get(user=user, course=course_item)
            message = 'subscribe is already exist'
        except Subscription.DoesNotExist:
            new_subscribe = Subscription.objects.create(user=user, course=course_item)
            message = 'subscribe is created'
        finally:
            return Response({"message": message})


class UnsubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        course_id = request.data["course_id"]
        course_item = Course.objects.get(pk=course_id)
        try:
            subs_item = Subscription.objects.get(user=user, course=course_item)
            Subscription.objects.get(user=user, course=course_item).delete()
            message = 'unsubscription completed successfully'
        except Subscription.DoesNotExist:
            message = 'subscription is not exist'
        finally:
            return Response({"message": message})


class CreateProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product = stripe.Product.create(
                name=request.data['name'],
                description=request.data.get('description', ''),
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(request.data['amount']),
                currency='usd',
            )
            return Response({'product_id': product.id, 'price_id': price.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class CreatePaymentIntentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(request.data['amount']),
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({'client_secret': intent.client_secret})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        signature_header = request.headers.get("Stripe-Signature")
        if not signature_header:
            return JsonResponse({"error": "Missing Stripe-Signature header"}, status=400)



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