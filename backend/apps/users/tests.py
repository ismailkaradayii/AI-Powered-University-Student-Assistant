"""
WBS 2.2 - Unit Tests for Student Authentication (TC-01 & TC-02)
Owner: İsmail Karadayı (20220236)
"""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class StudentAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            student_number="20220236",
            full_name="İsmail Karadayı",
            password="password123",
        )

    def test_tc01_valid_student_login_returns_jwt(self):
        """TC-01: Valid student number and password returns HTTP 200 and JWT token."""
        response = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["student_number"], "20220236")

    def test_tc02_invalid_password_returns_401(self):
        """TC-02: Invalid password returns HTTP 401 Unauthorized."""
        response = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
