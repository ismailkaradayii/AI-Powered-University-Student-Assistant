from django.contrib import admin
from .models import Announcement, Course, Exam


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "instructor", "day", "start_time", "end_time", "classroom")
    search_fields = ("code", "name", "instructor")
    list_filter = ("day",)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("course", "exam_type", "exam_date", "exam_time", "classroom")
    list_filter = ("exam_type", "exam_date")
    search_fields = ("course__code", "course__name")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "is_important", "created_at")
    list_filter = ("is_important",)
    search_fields = ("title", "content")
