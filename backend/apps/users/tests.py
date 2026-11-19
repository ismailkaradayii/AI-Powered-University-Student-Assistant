"""
WBS 2.1 & 2.2 - Comprehensive Unit Tests for Student Authentication & Permissions (TC-01 & TC-02)
Owner: İsmail Karadayı (20220236)
"""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class StudentAuthenticationTests(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            student_number="20220236",
            full_name="İsmail Karadayı",
            email="ismail@neu.edu.tr",
            department="Software Engineering",
            grade_year=4,
            password="password123",
        )
        self.admin_user = User.objects.create_superuser(
            student_number="20220001",
            full_name="NEU System Admin",
            password="adminpassword123",
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
        self.assertEqual(response.data["user"]["role"], "student")

    def test_tc02_invalid_password_returns_401(self):
        """TC-02: Valid student number with incorrect password returns HTTP 401 Unauthorized."""
        response = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_tc02_unknown_student_number_returns_401(self):
        """TC-02: Non-existent student number returns HTTP 401 Unauthorized."""
        response = self.client.post(
            "/api/auth/login/",
            {"student_number": "99999999", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_student_cannot_login_returns_403(self):
        """Inactive student account receives HTTP 403 Forbidden instead of JWT."""
        self.student.is_active = False
        self.student.save(update_fields=["is_active"])

        response = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("inactive", response.data["detail"].lower())

    def test_student_registration_hashes_password_and_returns_jwt(self):
        """POST /api/auth/register/ creates a hashed StudentUser and issues JWT tokens."""
        response = self.client.post(
            "/api/auth/register/",
            {
                "student_number": "20239999",
                "full_name": "Test Student",
                "email": "test.student@neu.edu.tr",
                "department": "Software Engineering",
                "grade_year": 3,
                "password": "securepassword123",
                "password_confirm": "securepassword123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        created_user = User.objects.get(student_number="20239999")
        self.assertNotEqual(created_user.password, "securepassword123")
        self.assertTrue(created_user.check_password("securepassword123"))

    def test_duplicate_student_number_registration_fails(self):
        """Registering an existing student_number returns HTTP 400 Bad Request."""
        response = self.client.post(
            "/api/auth/register/",
            {
                "student_number": "20220236",
                "full_name": "Duplicate Student",
                "password": "securepassword123",
                "password_confirm": "securepassword123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("student_number", response.data)

    def test_get_and_update_current_user_profile_with_jwt(self):
        """Authenticated student can retrieve and update profile via /api/auth/me/."""
        login_res = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "password123"},
            format="json",
        )
        access_token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        me_res = self.client.get("/api/auth/me/")
        self.assertEqual(me_res.status_code, status.HTTP_200_OK)
        self.assertEqual(me_res.data["full_name"], "İsmail Karadayı")

        patch_res = self.client.patch(
            "/api/auth/me/",
            {"department": "Computer Engineering", "is_staff": True},
            format="json",
        )
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.department, "Computer Engineering")
        # Privilege escalation must be ignored
        self.assertFalse(self.student.is_staff)

    def test_unauthorized_profile_access_returns_401(self):
        """Unauthenticated GET /api/auth/me/ returns HTTP 401 Unauthorized."""
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_success_and_wrong_old_password_rejected(self):
        """POST /api/auth/change-password/ verifies old password and updates hash."""
        login_res = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "password123"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_res.data['access']}")

        bad_res = self.client.post(
            "/api/auth/change-password/",
            {
                "old_password": "incorrect_old",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123",
            },
            format="json",
        )
        self.assertEqual(bad_res.status_code, status.HTTP_400_BAD_REQUEST)

        ok_res = self.client.post(
            "/api/auth/change-password/",
            {
                "old_password": "password123",
                "new_password": "newpassword123",
                "new_password_confirm": "newpassword123",
            },
            format="json",
        )
        self.assertEqual(ok_res.status_code, status.HTTP_200_OK)

        # Verify login succeeds with the new password
        self.client.credentials()
        relogin = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "newpassword123"},
            format="json",
        )
        self.assertEqual(relogin.status_code, status.HTTP_200_OK)

    def test_token_refresh_returns_new_access_token(self):
        """POST /api/auth/refresh/ issues a fresh JWT access token."""
        login_res = self.client.post(
            "/api/auth/login/",
            {"student_number": "20220236", "password": "password123"},
            format="json",
        )
        refresh_res = self.client.post(
            "/api/auth/refresh/",
            {"refresh": login_res.data["refresh"]},
            format="json",
        )
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_res.data)

    def test_admin_endpoints_manage_permissions_and_block_non_admins(self):
        """Admin endpoints allow staff to manage permissions and return 403 for normal students."""
        # Normal student must receive 403
        self.client.force_authenticate(user=self.student)
        forbidden_res = self.client.get("/api/auth/admin/students/")
        self.assertEqual(forbidden_res.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user lists and updates student permissions
        self.client.force_authenticate(user=self.admin_user)
        list_res = self.client.get("/api/auth/admin/students/?search=20220236")
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_res.data), 1)

        patch_res = self.client.patch(
            f"/api/auth/admin/students/{self.student.id}/",
            {"is_staff": True},
            format="json",
        )
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertTrue(self.student.is_staff)
