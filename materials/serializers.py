from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course' 'owner']

    def validate(self, attrs):
        if 'owner' in self.initial_data and self.context['request']:
            raise serializers.ValidationError('Вы не владелец.')
        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    def get_lesson_count(self, course):
        return len(Lesson.objects.filter(course=course))

    def get_lessons(self, course):
        return [LessonSerializer(lesson).data for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lesson_count', 'lessons', 'owner']

    def validate(self, attrs):
        if 'owner' in self.initial_data and self.context['request']:
            raise serializers.ValidationError('Вы не владелец.')
        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
