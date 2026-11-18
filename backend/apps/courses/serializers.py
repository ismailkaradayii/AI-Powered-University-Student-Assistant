"""
WBS 2.3 - Course, Exam & Announcement Serializers
Owner: Barış Avanoğlu (20220194)
"""
from rest_framework import serializers
from .models import Announcement, Course, Exam


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "code",
            "name",
            "instructor",
            "day",
            "start_time",
            "end_time",
            "classroom",
            "credits",
        ]


class ExamSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source="course.code", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Exam
        fields = [
            "id",
            "course",
            "course_code",
            "course_name",
            "exam_type",
            "exam_date",
            "exam_time",
            "classroom",
            "notes",
        ]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id", "title", "content", "is_important", "created_at", "updated_at"]
