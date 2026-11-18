"""
WBS 4.1 & 5.1 - Hybrid Query Router (Course/Exam SQLite Lookup + Regulation RAG)
Guarantees <3 second response time NFR (TC-03 & TC-04).
Owner: Mustafa Özgür Güdükboy (20220404)
"""
import re
import time
from apps.courses.models import Announcement, Course, Exam
from .rag_engine import generate_rag_answer


def answer_student_question(question: str) -> dict:
    """
    Routes student question:
    1. Checks if the query mentions a course code (e.g., SWE488) or exam/schedule inquiry (TC-03).
    2. Otherwise routes to the Regulation Knowledge Base RAG Engine (TC-04).
    """
    start_time = time.perf_counter()
    clean_q = question.strip()
    q_lower = clean_q.lower()

    # 1. Detect explicit course code pattern (e.g., SWE488, SWE401, AIC405)
    course_code_match = re.search(r"\b([A-Za-z]{3}\s*\d{3})\b", clean_q)
    if course_code_match:
        normalized_code = course_code_match.group(1).replace(" ", "").upper()
        course = Course.objects.filter(code__iexact=normalized_code).first()
        if course:
            exams = Exam.objects.filter(course=course)
            if "midterm" in q_lower or "exam" in q_lower or "final" in q_lower or "when" in q_lower:
                target_type = "Final" if "final" in q_lower else "Midterm"
                exam = exams.filter(exam_type__iexact=target_type).first() or exams.first()
                if exam:
                    elapsed_ms = max(1, int((time.perf_counter() - start_time) * 1000))
                    return {
                        "answer": (
                            f"The {course.code} ({course.name}) {exam.exam_type} exam is scheduled for "
                            f"{exam.exam_date} at {exam.exam_time} in classroom {exam.classroom}."
                        ),
                        "source_type": "DATABASE",
                        "citations": [f"SQLite DB: {course.code} - {exam.exam_type} Exam ({exam.exam_date})"],
                        "response_time_ms": elapsed_ms,
                    }

            elapsed_ms = max(1, int((time.perf_counter() - start_time) * 1000))
            return {
                "answer": (
                    f"{course.code} ({course.name}) is taught by {course.instructor} every {course.day} "
                    f"from {course.start_time} to {course.end_time} in classroom {course.classroom}."
                ),
                "source_type": "DATABASE",
                "citations": [f"SQLite DB: Course Schedule ({course.code})"],
                "response_time_ms": elapsed_ms,
            }

    # 2. Check general exam schedule / announcement queries
    if "announcement" in q_lower:
        latest = Announcement.objects.first()
        if latest:
            elapsed_ms = max(1, int((time.perf_counter() - start_time) * 1000))
            return {
                "answer": f"Latest Announcement — {latest.title}: {latest.content}",
                "source_type": "DATABASE",
                "citations": [f"SQLite DB: Announcement ({latest.title})"],
                "response_time_ms": elapsed_ms,
            }

    # 3. Route to Regulation Knowledge Base RAG Engine (TC-04)
    rag_answer, citations = generate_rag_answer(clean_q)
    elapsed_ms = max(1, int((time.perf_counter() - start_time) * 1000))
    return {
        "answer": rag_answer,
        "source_type": "RAG",
        "citations": citations,
        "response_time_ms": elapsed_ms,
    }
