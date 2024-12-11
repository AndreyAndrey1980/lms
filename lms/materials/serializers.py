from rest_framework import serializers
from .models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return len(Lesson.objects.filter(course=course))

    def get_lessons(self, course):
        lessons = [LessonSerializer(lesson).data for lesson in Lesson.objects.filter(course=course)]
        return lessons

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lesson_count', 'lessons']
