"""
WBS 2.2 - Django Admin User Management Configuration
Owner: İsmail Karadayı (20220236)
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentUser


@admin.register(StudentUser)
class StudentUserAdmin(UserAdmin):
    model = StudentUser
    list_display = (
        "student_number",
        "full_name",
        "department",
        "grade_year",
        "is_staff",
        "is_active",
        "last_login",
    )
    list_filter = ("department", "grade_year", "is_staff", "is_active")
    search_fields = ("student_number", "full_name", "email")
    ordering = ("student_number",)
    readonly_fields = ("created_at", "updated_at", "last_login")
    actions = ["activate_students", "deactivate_students", "grant_admin_access"]

    fieldsets = (
        (None, {"fields": ("student_number", "password")}),
        ("Personal Info", {"fields": ("full_name", "email", "department", "grade_year")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Audit Timestamps", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "student_number",
                    "full_name",
                    "email",
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

    @admin.action(description="Activate selected student accounts")
    def activate_students(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected student accounts")
    def deactivate_students(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Grant admin (staff) permissions to selected users")
    def grant_admin_access(self, request, queryset):
        queryset.update(is_staff=True)
