from rest_framework import serializers
from .models import Payments, User
from materials.serializers import LessonSerializer, CourseSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['user', 'date', 'subject', 'amount', 'pay_method', 'lesson', 'course']
