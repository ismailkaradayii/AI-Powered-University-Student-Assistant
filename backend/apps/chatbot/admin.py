from django.contrib import admin
from .models import ChatQueryLog


@admin.register(ChatQueryLog)
class ChatQueryLogAdmin(admin.ModelAdmin):
    list_display = ("question", "source_type", "response_time_ms", "created_at")
    list_filter = ("source_type",)
    search_fields = ("question", "answer")
