"""
WBS 4.1 & 5.1 - Unit Tests for AI Chatbot & RAG Engine (<3s NFR, TC-03 & TC-04)
Owner: Mustafa Özgür Güdükboy (20220404)
"""
from datetime import date
from rest_framework import status
from rest_framework.test import APITestCase
from apps.courses.models import Course, Exam


class ChatbotRAGTests(APITestCase):
    def setUp(self):
        course = Course.objects.create(
            code="SWE488",
            name="Software Implementation",
            instructor="Dr. NEU",
            day="Wednesday",
            start_time="09:00",
            end_time="12:00",
            classroom="FE-101",
        )
        Exam.objects.create(
            course=course,
            exam_type="Midterm",
            exam_date=date(2026, 11, 10),
            exam_time="10:00",
            classroom="Amfi-2",
        )

    def test_tc03_course_exam_query_under_3_seconds(self):
        """TC-03: Chatbot recognizes SWE488 and returns exam date in <3000ms."""
        response = self.client.post(
            "/api/chatbot/ask/",
            {"question": "When is the SWE488 midterm exam?"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("2026-11-10", response.data["answer"])
        self.assertLess(response.data["response_time_ms"], 3000)

    def test_tc04_regulation_rag_query_quotes_article(self):
        """TC-04: RAG engine quotes Article 14 for add-drop rules without hallucinating."""
        response = self.client.post(
            "/api/chatbot/ask/",
            {"question": "What are the course add-drop rules?"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Article 14", response.data["answer"])
        self.assertEqual(response.data["source_type"], "RAG")
