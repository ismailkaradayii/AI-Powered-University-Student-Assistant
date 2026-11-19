"""
WBS 2.2 - Custom Role-Based Authorization Permissions
Owner: İsmail Karadayı (20220236)
"""
from rest_framework import permissions


class IsAdminStudent(permissions.BasePermission):
    """Grants access only to authenticated users with admin/staff privileges."""

    message = "Admin privileges are required to perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_staff
        )


class IsActiveStudent(permissions.BasePermission):
    """Grants access only to active, authenticated student users."""

    message = "Your student account is inactive. Please contact Student Affairs."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
