from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, CourseViewSet, ExamViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"exams", ExamViewSet, basename="exam")
router.register(r"announcements", AnnouncementViewSet, basename="announcement")

urlpatterns = [
    path("", include(router.urls)),
]
