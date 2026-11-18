"""
WBS 2.2 - JWT Authentication & User Endpoints (TC-01 & TC-02)
Owner: İsmail Karadayı (20220236)
"""
from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import StudentLoginSerializer, StudentUserSerializer


class StudentLoginView(APIView):
    """
    POST /api/auth/login/
    TC-01: Valid student_number & password -> HTTP 200 with JWT access/refresh tokens.
    TC-02: Invalid password -> HTTP 401 Unauthorized with informative error message.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_number = serializer.validated_data["student_number"].strip()
        password = serializer.validated_data["password"]

        user = authenticate(
            request, username=student_number, password=password
        )
        if user is None or not user.is_active:
            return Response(
                {
                    "detail": "Invalid student number or password. Please check your credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": StudentUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class CurrentUserView(APIView):
    """
    GET /api/auth/me/
    Returns authenticated student's profile information.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(StudentUserSerializer(request.user).data)
