"""
Seeds initial university users, courses, exams, and announcements for SWE488 testing (TC-01 to TC-05).
Usage: python manage.py seed_data
"""
from datetime import date
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from apps.courses.models import Announcement, Course, Exam

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds initial SWE488 students, courses, exams, and announcements into SQLite."

    def handle(self, *args, **options):
        team_members = [
            ("20220236", "İsmail Karadayı", True),
            ("20220194", "Barış Avanoğlu", True),
            ("20220404", "Mustafa Özgür Güdükboy", False),
            ("20230147", "Rabia Basan", False),
            ("20211046", "Fatih Yazıcı", True),
        ]

        for student_no, full_name, is_admin in team_members:
            user, created = User.objects.get_or_create(
                student_number=student_no,
                defaults={
                    "full_name": full_name,
                    "department": "Software Engineering",
                    "grade_year": 4,
                    "is_staff": is_admin,
                    "is_superuser": is_admin,
                },
            )
            if created:
                user.set_password("password123")
                user.save()

        courses_data = [
            {
                "code": "SWE488",
                "name": "Software Implementation",
                "instructor": "Assoc. Prof. Dr. NEU Instructor",
                "day": "Wednesday",
                "start_time": "09:00",
                "end_time": "12:00",
                "classroom": "FE-101",
                "credits": 4,
            },
            {
                "code": "SWE401",
                "name": "Software Architecture & Design",
                "instructor": "Prof. Dr. Engineering Faculty",
                "day": "Monday",
                "start_time": "13:00",
                "end_time": "16:00",
                "classroom": "FE-204",
                "credits": 3,
            },
            {
                "code": "AIC405",
                "name": "Artificial Intelligence & NLP",
                "instructor": "Asst. Prof. Dr. AI Lab",
                "day": "Thursday",
                "start_time": "10:00",
                "end_time": "13:00",
                "classroom": "AI-Lab-1",
                "credits": 4,
            },
        ]

        for c in courses_data:
            course, _ = Course.objects.update_or_create(code=c["code"], defaults=c)
            if c["code"] == "SWE488":
                Exam.objects.update_or_create(
                    course=course,
                    exam_type="Midterm",
                    defaults={
                        "exam_date": date(2026, 11, 10),
                        "exam_time": "10:00",
                        "classroom": "Amfi-2",
                        "notes": "Bring student ID card. Closed book examination.",
                    },
                )
                Exam.objects.update_or_create(
                    course=course,
                    exam_type="Final",
                    defaults={
                        "exam_date": date(2027, 1, 5),
                        "exam_time": "14:00",
                        "classroom": "Amfi-1",
                        "notes": "Final project & comprehensive exam.",
                    },
                )
            elif c["code"] == "SWE401":
                Exam.objects.update_or_create(
                    course=course,
                    exam_type="Midterm",
                    defaults={
                        "exam_date": date(2026, 11, 12),
                        "exam_time": "11:30",
                        "classroom": "FE-204",
                        "notes": "UML Diagrams & Architecture Patterns.",
                    },
                )

        Announcement.objects.get_or_create(
            title="2026-2027 Fall Midterm Examination Schedule",
            defaults={
                "content": "Midterm examinations will take place between 07 November 2026 and 14 November 2026. Please check your course schedule and exam classrooms.",
                "is_important": True,
            },
        )
        Announcement.objects.get_or_create(
            title="Course Withdrawal Deadline Reminder",
            defaults={
                "content": "The last day for course withdrawal is 18 December 2026. Consult your academic advisor before submitting a withdrawal request.",
                "is_important": False,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully seeded 5 team members (password: password123), courses, exams (SWE488), and announcements!"
            )
        )
