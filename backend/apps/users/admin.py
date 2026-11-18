from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentUser


@admin.register(StudentUser)
class StudentUserAdmin(UserAdmin):
    model = StudentUser
    list_display = ("student_number", "full_name", "department", "grade_year", "is_staff", "is_active")
    list_filter = ("department", "grade_year", "is_staff", "is_active")
    search_fields = ("student_number", "full_name", "email")
    ordering = ("student_number",)

    fieldsets = (
        (None, {"fields": ("student_number", "password")}),
        ("Personal Info", {"fields": ("full_name", "email", "department", "grade_year")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "student_number",
                    "full_name",
                    "department",
                    "grade_year",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
