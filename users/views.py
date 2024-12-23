from django.shortcuts import render
from rest_framework import viewsets
from .models import Payments, User
from .serializers import PaymentsSerializer, UserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['pay_method', 'lesson', 'course']
    ordering_fields = ['date']


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (IsAuthenticated,)
