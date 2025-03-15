from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import Lesson, Course
from .validators import validate_video_url
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'owner']

    def validate(self, attrs):
        if 'owner' in self.initial_data and self.context['request']:
            raise serializers.ValidationError('Вы не владелец.')
        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    is_subscribe = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_is_subscribe(self, course):
        user = self.context['request'].user
        try:
            subs_item = Subscription.objects.get(user=user, course=course)
            return True
        except Subscription.DoesNotExist:
            return False

    def get_lesson_count(self, course):
        return len(Lesson.objects.filter(course=course))

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'amount', 'preview', 'lesson_count', 'lessons', 'owner', 'is_subscribe']

    def validate(self, attrs):
        if 'owner' in self.initial_data and self.context['request']:
            raise serializers.ValidationError('Вы не владелец.')
        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
