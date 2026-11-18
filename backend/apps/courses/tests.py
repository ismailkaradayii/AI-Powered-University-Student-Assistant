"""
WBS 2.3 - Unit Tests for Course, Exam & Admin Panel Data Updates (TC-05)
Owner: Barış Avanoğlu (20220194)
"""
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Exam

User = get_user_model()


class CourseExamAdminTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            student_number="20220194",
            full_name="Barış Avanoğlu",
            password="password123",
        )
        self.course = Course.objects.create(
            code="SWE488",
            name="Software Implementation",
            instructor="Dr. NEU",
            day="Wednesday",
            start_time="09:00",
            end_time="12:00",
            classroom="FE-101",
        )
        self.exam = Exam.objects.create(
            course=self.course,
            exam_type="Midterm",
            exam_date=date(2026, 11, 10),
            exam_time="10:00",
            classroom="Amfi-2",
        )

    def test_tc05_admin_updates_announcement_and_exam(self):
        """TC-05: Admin user creates announcement and updates exam schedule in SQLite."""
        self.client.force_authenticate(user=self.admin_user)
        ann_res = self.client.post(
            "/api/announcements/",
            {
                "title": "Midterm Room Update",
                "content": "SWE488 Midterm will be held in Amfi-2.",
                "is_important": True,
            },
            format="json",
        )
        self.assertEqual(ann_res.status_code, status.HTTP_201_CREATED)
