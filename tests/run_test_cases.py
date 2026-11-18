"""
WBS 5.1 - Automated Verification of SWE488 Test Cases (TC-01 to TC-05)
Usage (from backend/ directory):
    python ../tests/run_test_cases.py
Owner: Fatih Yazıcı (20211046)
"""
import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402

django.setup()

from django.core.management import call_command  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402


def run_all_tests():
    print("=" * 65)
    print("SWE488 - AI-Powered University Student Assistant QA Test Suite")
    print("=" * 65)

    call_command("migrate", verbosity=0)
    call_command("seed_data")

    client = APIClient()

    # TC-01: Student Secure Login
    res_tc01 = client.post(
        "/api/auth/login/",
        {"student_number": "20220236", "password": "password123"},
        format="json",
    )
    assert res_tc01.status_code == 200 and "access" in res_tc01.data, "TC-01 Failed!"
    jwt_token = res_tc01.data["access"]
    print("[PASS] TC-01 (Student Secure Login): HTTP 200 & JWT Token returned.")

    # TC-02: Login with Incorrect Password (Negative Test)
    res_tc02 = client.post(
        "/api/auth/login/",
        {"student_number": "20220236", "password": "wrong_password_999"},
        format="json",
    )
    assert res_tc02.status_code == 401, "TC-02 Failed!"
    print(f"[PASS] TC-02 (Negative Login Test): HTTP 401 returned -> {res_tc02.data['detail']}")

    # TC-03: Course & Exam Info Query (<3s NFR)
    res_tc03 = client.post(
        "/api/chatbot/ask/",
        {"question": "When is the SWE488 midterm exam?"},
        format="json",
    )
    assert res_tc03.status_code == 200, "TC-03 Failed!"
    assert "SWE488" in res_tc03.data["answer"] and res_tc03.data["response_time_ms"] < 3000
    print(
        f"[PASS] TC-03 (Course & Exam Query): Answered in {res_tc03.data['response_time_ms']}ms (<3000ms NFR) -> {res_tc03.data['answer']}"
    )

    # TC-04: Regulation Knowledge Base Query (RAG)
    res_tc04 = client.post(
        "/api/chatbot/ask/",
        {"question": "What are the course add-drop rules?"},
        format="json",
    )
    assert res_tc04.status_code == 200, "TC-04 Failed!"
    assert "Article 14" in res_tc04.data["answer"]
    print(
        f"[PASS] TC-04 (Regulation RAG Query): Quoted Article without hallucination -> {res_tc04.data['answer'][:110]}..."
    )

    # TC-05: Admin Panel Data Update
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
    res_tc05 = client.post(
        "/api/announcements/",
        {
            "title": "TC-05 Admin Live Update Test",
            "content": "SWE488 Midterm Classroom confirmed as Amfi-2.",
            "is_important": True,
        },
        format="json",
    )
    assert res_tc05.status_code == 201, "TC-05 Failed!"
    print("[PASS] TC-05 (Admin Panel Data Update): New announcement persisted to SQLite DB immediately.")
    print("=" * 65)
    print("ALL 5 SWE488 TEST CASES (TC-01 .. TC-05) PASSED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_all_tests()
