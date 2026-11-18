"""
WBS 4.1 & 5.1 - Chatbot Query History & NFR Performance Log (<3s Target)
Owner: Mustafa Özgür Güdükboy (20220404)
"""
from django.conf import settings
from django.db import models


class ChatQueryLog(models.Model):
    SOURCE_CHOICES = [
        ("DATABASE", "Course & Exam SQLite DB"),
        ("RAG", "Regulation Vector KB (RAG)"),
        ("HYBRID", "Hybrid DB + RAG"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chat_logs",
    )
    question = models.TextField()
    answer = models.TextField()
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="RAG")
    response_time_ms = models.PositiveIntegerField(help_text="Execution time in milliseconds (<3000ms NFR)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.source_type} - {self.response_time_ms}ms] {self.question[:50]}"
