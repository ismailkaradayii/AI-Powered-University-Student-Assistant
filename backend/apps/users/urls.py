"""
WBS 2.2 - Authentication & User Management URL Routes
Owner: İsmail Karadayı (20220236)
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AdminStudentDetailView,
    AdminStudentListView,
    ChangePasswordView,
    CurrentUserView,
    StudentLoginView,
    StudentRegisterView,
)

urlpatterns = [
    path("login/", StudentLoginView.as_view(), name="student-login"),
    path("register/", StudentRegisterView.as_view(), name="student-register"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("admin/students/", AdminStudentListView.as_view(), name="admin-student-list"),
    path("admin/students/<int:pk>/", AdminStudentDetailView.as_view(), name="admin-student-detail"),
]
