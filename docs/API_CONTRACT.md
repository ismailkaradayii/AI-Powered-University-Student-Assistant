# API Contract & Integration Specification (SWE488)

Bu doküman, **Backend (Django REST Framework)** ve **Frontend (Next.js)** geliştiricilerinin birbirini beklemeden paralel çalışabilmesi için standart JSON veri yapılarını ve endpoint adreslerini tanımlar.

**Base URL (Local Development):** `http://127.0.0.1:8000/api`

---

## 1. Authentication & Users (`apps/users` - İsmail Karadayı)

### `POST /api/auth/login/` (TC-01 & TC-02)
Öğrenci numarası ve şifre ile giriş yapar, JWT token döndürür.

- **Request Body:**
```json
{
  "student_number": "20220236",
  "password": "password123"
}
```
- **Success Response (`200 OK` - TC-01):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR...",
  "user": {
    "id": 1,
    "student_number": "20220236",
    "full_name": "İsmail Karadayı",
    "department": "Software Engineering",
    "is_staff": true
  }
}
```
- **Error Response (`401 Unauthorized` - TC-02):**
```json
{
  "detail": "Invalid student number or password. Please check your credentials."
}
```

### `GET /api/auth/me/`
Header'da `Authorization: Bearer <access_token>` ile giriş yapmış kullanıcının bilgilerini döndürür.

---

## 2. Courses, Exams & Announcements (`apps/courses` - Barış Avanoğlu)

### `GET /api/courses/`
Haftalık ders programını listeler.
- **Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "code": "SWE488",
    "name": "Software Implementation",
    "instructor": "Dr. Instructor",
    "day": "Wednesday",
    "start_time": "09:00",
    "end_time": "12:00",
    "classroom": "FE-101"
  }
]
```

### `GET /api/exams/` & `POST /api/exams/` & `PUT /api/exams/<id>/` (TC-03 & TC-05)
Sınav tarihlerini listeler ve Admin yetkisiyle günceller.
- **Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "course_code": "SWE488",
    "course_name": "Software Implementation",
    "exam_type": "Midterm",
    "exam_date": "2026-11-10",
    "exam_time": "10:00",
    "classroom": "Amfi-2"
  }
]
```

### `GET /api/announcements/` & `POST /api/announcements/` (TC-05)
Duyuruları listeler ve Admin panelinden yeni duyuru ekler.
- **Response (`200 OK`):**
```json
[
  {
    "id": 1,
    "title": "2026-2027 Fall Midterm Schedule Announced",
    "content": "Midterm exams will be held between 07 - 14 November 2026.",
    "created_at": "2026-11-01T10:00:00Z",
    "is_important": true
  }
]
```

---

## 3. AI Chatbot & RAG Engine (`apps/chatbot` - Mustafa Özgür Güdükboy)

### `POST /api/chatbot/ask/` (TC-03 & TC-04, NFR < 3.0s)
Öğrencinin doğal dilde sorduğu soruyu analiz eder:
1. Eğer soru ders kodu veya sınav tarihi içeriyorsa (`SWE488`, `midterm`, `final`, `schedule`), doğrudan SQLite veritabanından milisaniyeler içinde kesin bilgiyi çeker (**TC-03**).
2. Eğer soru üniversite yönetmeliği ile ilgiliyse (`add-drop`, `attendance`, `GPA`, `regulations`), Vector DB (LangChain + OpenAI RAG) üzerinden **Strict Context Prompting** ile ilgili yönetmelik maddesini kaynak göstererek yanıtlar (**TC-04**).

- **Request Body:**
```json
{
  "question": "When is the SWE488 midterm exam?"
}
```
- **Success Response (`200 OK`):**
```json
{
  "answer": "The SWE488 (Software Implementation) Midterm exam is scheduled for 2026-11-10 at 10:00 in classroom Amfi-2.",
  "source_type": "DATABASE",
  "citations": ["Course & Exam DB: SWE488 - Midterm"],
  "response_time_ms": 145
}
```
