"""
WBS 2.2 - Authentication & User Serializers
Owner: İsmail Karadayı (20220236)
"""
from rest_framework import serializers
from .models import StudentUser


class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUser
        fields = [
            "id",
            "student_number",
            "full_name",
            "email",
            "department",
            "grade_year",
            "is_staff",
        ]


class StudentLoginSerializer(serializers.Serializer):
    student_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
