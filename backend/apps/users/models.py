"""
WBS 2.1 & 2.2 - Student Authentication & User Models
Owner: İsmail Karadayı (20220236)
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class StudentUserManager(BaseUserManager):
    """Custom manager where student_number is the unique identifier for authentication."""

    def create_user(self, student_number, password=None, **extra_fields):
        cleaned_number = str(student_number or "").strip()
        if not cleaned_number:
            raise ValueError("The Student Number field must be set.")
        extra_fields.setdefault("is_active", True)
        user = self.model(student_number=cleaned_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(student_number, password, **extra_fields)


class StudentUser(AbstractBaseUser, PermissionsMixin):
    student_number = models.CharField(max_length=20, unique=True, db_index=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=120, default="Software Engineering")
    grade_year = models.PositiveSmallIntegerField(default=4)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StudentUserManager()

    USERNAME_FIELD = "student_number"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "Student User"
        verbose_name_plural = "Student Users"
        ordering = ["student_number"]

    @property
    def role(self) -> str:
        return "admin" if self.is_staff else "student"

    def __str__(self):
        return f"{self.student_number} - {self.full_name}"
