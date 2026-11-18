"""
WBS 4.1 - AI Chatbot API Endpoint (TC-03 & TC-04)
Owner: Mustafa Özgür Güdükboy (20220404)
"""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatQueryLog
from .serializers import ChatbotAskSerializer, ChatQueryLogSerializer
from .services import answer_student_question


class ChatbotAskView(APIView):
    """
    POST /api/chatbot/ask/
    Answers questions regarding regulations (RAG) and course/exam timetables (DB) in <3 seconds.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ChatbotAskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        result = answer_student_question(question)

        user = request.user if request.user and request.user.is_authenticated else None
        ChatQueryLog.objects.create(
            user=user,
            question=question,
            answer=result["answer"],
            source_type=result["source_type"],
            response_time_ms=result["response_time_ms"],
        )

        return Response(result, status=status.HTTP_200_OK)


class ChatbotHistoryView(APIView):
    """
    GET /api/chatbot/history/
    Returns recent chatbot queries and NFR response time metrics.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        logs = ChatQueryLog.objects.all()[:20]
        return Response(ChatQueryLogSerializer(logs, many=True).data)
