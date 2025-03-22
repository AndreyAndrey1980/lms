from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from .models import Payments, User, Subscription
from .serializers import PaymentsSerializer, UserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from materials.models import Course, Lesson
from rest_framework.response import Response
from rest_framework.decorators import action
from users.stripe import create_session


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['pay_method', 'lesson', 'course']
    ordering_fields = ['date']

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        try:
            user = request.user
            subject_type = request.data.get('subject')
            course_id = request.data.get('course_id')
            lesson_id = request.data.get('lesson_id')
            amount = int(request.data.get('amount'))

            if subject_type == Payments.SubjectType.COURSE:
                course: Course | None = get_object_or_404(Course, id=course_id)
                subject_name = course.name
                subject_desc = course.description
                session = create_session(subject_name, amount)
                serializer = self.get_serializer(data={"user": request.user, "course":course})
            elif subject_type == Payments.SubjectType.LESSON:
                lesson: Lesson | None = get_object_or_404(Lesson, id=lesson_id)
                subject_name = lesson.title
                subject_desc = lesson.description
                session = create_session(subject_name, amount)
                serializer = self.get_serializer(data={"user": request.user, "lesson":lesson})
            else:
                return Response({'error': 'Invalid subject type'}, status=400)
            serializer.save()
            return Response({'session_id': session.id, 'stripe_url': session.url})

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=400)


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
