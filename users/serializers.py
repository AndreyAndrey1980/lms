from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Payments, User
from materials.serializers import LessonSerializer, CourseSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']


class PaymentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()
    lesson = LessonSerializer()
    class Meta:
        model = Payments
        fields = ['user', 'date', 'subject', 'amount', 'pay_method', 'lesson', 'course']
