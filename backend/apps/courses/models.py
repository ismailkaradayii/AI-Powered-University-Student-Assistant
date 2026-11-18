"""
WBS 2.1 & 2.3 - Course, Exam & Announcement Models
Owner: Barış Avanoğlu (20220194)
"""
from django.db import models


class Course(models.Model):
    DAYS_OF_WEEK = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    ]

    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    instructor = models.CharField(max_length=120)
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    start_time = models.CharField(max_length=10, help_text="Format: HH:MM (e.g., 09:00)")
    end_time = models.CharField(max_length=10, help_text="Format: HH:MM (e.g., 12:00)")
    classroom = models.CharField(max_length=50)
    credits = models.PositiveSmallIntegerField(default=3)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Exam(models.Model):
    EXAM_TYPES = [
        ("Midterm", "Midterm"),
        ("Final", "Final"),
        ("Make-up", "Make-up"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default="Midterm")
    exam_date = models.DateField()
    exam_time = models.CharField(max_length=10, help_text="Format: HH:MM (e.g., 10:00)")
    classroom = models.CharField(max_length=50)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["exam_date", "exam_time"]

    def __str__(self):
        return f"{self.course.code} ({self.exam_type}) - {self.exam_date}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
