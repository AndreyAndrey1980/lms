from django.shortcuts import render
from rest_framework import viewsets
from .models import Payments
from .serializers import PaymentsSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['pay_method', 'lesson', 'course']
    ordering_fields = ['date']

