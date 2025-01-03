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


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['pay_method', 'lesson', 'course']
    ordering_fields = ['date']


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
