from rest_framework import serializers
from .models import ChatQueryLog


class ChatbotAskSerializer(serializers.Serializer):
    question = serializers.CharField(required=True, max_length=1000)


class ChatQueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatQueryLog
        fields = [
            "id",
            "question",
            "answer",
            "source_type",
            "response_time_ms",
            "created_at",
        ]
