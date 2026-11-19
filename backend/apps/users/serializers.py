"""
WBS 2.2 - Authentication, Registration, Profile & Admin Serializers
Owner: İsmail Karadayı (20220236)
"""
from rest_framework import serializers
from .models import StudentUser


class StudentUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

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
            "is_active",
            "role",
            "created_at",
        ]
        read_only_fields = ["id", "student_number", "is_staff", "is_active", "role", "created_at"]


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    """Allows students to update their personal profile fields without escalating privileges."""

    class Meta:
        model = StudentUser
        fields = ["full_name", "email", "department", "grade_year"]

    def validate_grade_year(self, value):
        if not 1 <= value <= 6:
            raise serializers.ValidationError("Grade year must be between 1 and 6.")
        return value


class StudentLoginSerializer(serializers.Serializer):
    student_number = serializers.CharField(required=True, allow_blank=False, trim_whitespace=True)
    password = serializers.CharField(required=True, allow_blank=False, write_only=True)


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = StudentUser
        fields = [
            "student_number",
            "full_name",
            "email",
            "department",
            "grade_year",
            "password",
            "password_confirm",
        ]

    def validate_student_number(self, value):
        cleaned = value.strip()
        if not cleaned.isdigit():
            raise serializers.ValidationError("Student number must contain only digits.")
        if len(cleaned) < 6:
            raise serializers.ValidationError("Student number must be at least 6 digits.")
        if StudentUser.objects.filter(student_number=cleaned).exists():
            raise serializers.ValidationError("A student with this student number already exists.")
        return cleaned

    def validate_grade_year(self, value):
        if not 1 <= value <= 6:
            raise serializers.ValidationError("Grade year must be between 1 and 6.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        return StudentUser.objects.create_user(password=password, **validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "New passwords do not match."})
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from the current password."}
            )
        return attrs


class AdminStudentManagementSerializer(serializers.ModelSerializer):
    """Admin-only serializer to manage user roles and account activation status."""

    role = serializers.CharField(read_only=True)

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
            "is_active",
            "role",
            "created_at",
            "last_login",
        ]
        read_only_fields = ["id", "student_number", "created_at", "last_login"]
