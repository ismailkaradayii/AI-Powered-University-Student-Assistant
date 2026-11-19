"""
WBS 2.2 - JWT Authentication, Registration, Profile & Admin Endpoints (TC-01 & TC-02)
Owner: İsmail Karadayı (20220236)
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import StudentUser
from .permissions import IsActiveStudent, IsAdminStudent
from .serializers import (
    AdminStudentManagementSerializer,
    ChangePasswordSerializer,
    StudentLoginSerializer,
    StudentProfileUpdateSerializer,
    StudentRegisterSerializer,
    StudentUserSerializer,
)


def _generate_jwt_payload(user: StudentUser) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": StudentUserSerializer(user).data,
    }


class StudentLoginView(APIView):
    """
    POST /api/auth/login/
    TC-01: Valid student_number & password -> HTTP 200 with JWT access/refresh tokens.
    TC-02: Invalid password or unknown student number -> HTTP 401 Unauthorized.
    Inactive accounts -> HTTP 403 Forbidden.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_number = serializer.validated_data["student_number"].strip()
        password = serializer.validated_data["password"]

        existing_user = StudentUser.objects.filter(student_number=student_number).first()
        if existing_user is not None and not existing_user.is_active:
            if existing_user.check_password(password):
                return Response(
                    {
                        "detail": "Your student account is inactive. Please contact Student Affairs."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        user = authenticate(request, username=student_number, password=password)
        if user is None:
            return Response(
                {
                    "detail": "Invalid student number or password. Please check your credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        update_last_login(None, user)
        return Response(_generate_jwt_payload(user), status=status.HTTP_200_OK)


class StudentRegisterView(APIView):
    """
    POST /api/auth/register/
    Registers a new student with securely hashed password and issues JWT tokens.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        update_last_login(None, user)
        return Response(_generate_jwt_payload(user), status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):
    """
    GET /api/auth/me/ -> Returns authenticated student's profile.
    PATCH /api/auth/me/ -> Updates authenticated student's own profile details.
    """

    permission_classes = [IsActiveStudent]

    def get(self, request):
        return Response(StudentUserSerializer(request.user).data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = StudentProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(StudentUserSerializer(request.user).data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Verifies current password and securely hashes the new password.
    """

    permission_classes = [IsActiveStudent]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password", "updated_at"])
        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )


class AdminStudentListView(APIView):
    """
    GET /api/auth/admin/students/
    Admin-only endpoint listing all registered student accounts (supports ?search= and ?role=).
    """

    permission_classes = [IsAdminStudent]

    def get(self, request):
        queryset = StudentUser.objects.all()
        search = request.query_params.get("search", "").strip()
        role = request.query_params.get("role", "").strip().lower()

        if search:
            queryset = queryset.filter(student_number__icontains=search) | queryset.filter(
                full_name__icontains=search
            )
        if role == "admin":
            queryset = queryset.filter(is_staff=True)
        elif role == "student":
            queryset = queryset.filter(is_staff=False)

        serializer = AdminStudentManagementSerializer(queryset.distinct(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminStudentDetailView(APIView):
    """
    GET/PATCH /api/auth/admin/students/<id>/
    Admin-only endpoint to inspect or update a student's permissions (is_staff, is_active).
    """

    permission_classes = [IsAdminStudent]

    def get(self, request, pk):
        student = get_object_or_404(StudentUser, pk=pk)
        return Response(
            AdminStudentManagementSerializer(student).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        student = get_object_or_404(StudentUser, pk=pk)
        serializer = AdminStudentManagementSerializer(
            student, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
