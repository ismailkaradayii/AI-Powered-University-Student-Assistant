"""
WBS 2.3 - Course, Exam & Announcement REST APIs (TC-03 & TC-05)
Owner: Barış Avanoğlu (20220194)
"""
from rest_framework import permissions, viewsets
from .models import Announcement, Course, Exam
from .serializers import AnnouncementSerializer, CourseSerializer, ExamSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access to students/everyone,
    and write/update/delete access only to admin/staff users (TC-05).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related("course").all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrReadOnly]


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]
