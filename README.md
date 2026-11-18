# AI-Powered University Student Assistant (SWE488)

**Course:** SWE488 - Software Implementation  
**Project Title:** AI-Powered University Student Assistant  
**Repository:** `https://github.com/ismailkaradayii/AI-Powered-University-Student-Assistant.git`

---

## 1. Proje Ekibi ve Adil Görev Dağılımı (5 Kişilik Eşit İş Bölümü)

Projede yer alan 5 ekip üyesinin her biri, birbirinin kodunu ezmeden (sıfır *merge conflict*) bağımsız modüller üzerinde çalışıp kendi branch'ine ve `main` branch'ine katkı sağlayacak şekilde eşit iş yüküyle görevlendirilmiştir:

| # | Ekip Üyesi | Öğrenci No | Sorumlu Olduğu Modül & Klasör | WBS ID | Test Senaryoları | Git Branch Adı |
|---|---|---|---|---|---|---|
| **1** | **İsmail Karadayı** | `20220236` | **Backend Auth & Users:** Custom `StudentUser` modeli, şifre hashleme, JWT Login/Refresh/Me API'leri, HTTP 401 hata yönetimi ve Django Admin kullanıcı yetkilendirmesi (`backend/apps/users/`) | `1.2`, `2.1`, `2.2` | `TC-01`, `TC-02` | `feature/ismail-auth-users` |
| **2** | **Barış Avanoğlu** | `20220194` | **Backend Course, Exam & Announcements:** Ders programı (`Course`), sınav takvimi (`Exam`) ve duyuru (`Announcement`) modelleri, CRUD REST API'leri, Admin izin kontrolü ve `seed_data` komutu (`backend/apps/courses/`) | `2.1`, `2.3` | `TC-03` (DB), `TC-05` (API) | `feature/baris-courses-exams` |
| **3** | **Mustafa Özgür Güdükboy** | `20220404` | **Backend AI & RAG Engine:** Üniversite yönetmelik bilgi tabanı indeksleme, LangChain/OpenAI RAG, *Strict Context Prompting* (Hallucination önleme - Risk R2) ve `<3s` NFR hibrit sorgu yönlendirici (`backend/apps/chatbot/`, `backend/data/regulations/`) | `4.1`, `5.1` | `TC-03` (AI), `TC-04` (RAG) | `feature/mustafa-ai-rag-chatbot` |
| **4** | **Rabia Basan** | `20230147` | **Frontend Auth & Student Dashboard:** Next.js + Tailwind CSS tasarım sistemi, JWT API istemcisi, `/pages/login` sayfası (TC-01 yönlendirme & TC-02 kırmızı hata mesajı) ve `/pages/dashboard` öğrenci paneli (`frontend/src/pages/login.js`, `dashboard.js`, `Layout.jsx`) | `3.1`, `3.2` | `TC-01`, `TC-02` (UI) | `feature/rabia-frontend-auth-dashboard` |
| **5** | **Fatih Yazıcı** | `20211046` | **Frontend Chatbot UI, Admin UI & QA/DevOps:** Canlı AI Chatbot bileşeni (`ChatbotWidget.jsx`), `/pages/admin` veri güncelleme arayüzü (TC-05), Postman & Otomatik Test Paketi (`tests/`) ve Vercel/PythonAnywhere Deployment (`vercel.json`, `Procfile`) | `4.2`, `5.1`, `5.2` | `TC-03`, `TC-04`, `TC-05` (UI & QA) | `feature/fatih-chatbot-ui-admin-qa` |

---

## 2. Teknoloji Yığını (Technology Stack)

- **Backend:** Python, Django 5, Django REST Framework (DRF), SimpleJWT
- **Frontend:** Next.js 14 (React), Tailwind CSS
- **Database:** SQLite (Geliştirme ortamı) / PostgreSQL uyumlu
- **AI & RAG Engine:** OpenAI API, LangChain, Vector Search & Strict Context Prompting (`< 3 saniye` NFR yanıt hedefi)
- **Testing & Deployment:** Postman Collection, Automated Python QA Suite, Vercel (Frontend), Render / PythonAnywhere (Backend)

---

## 3. Hızlı Kurulum ve Çalıştırma (Quick Start)

### A. Backend (Django REST API) Kurulumu
```bash
cd backend
python -m venv venv
# Windows için:
venv\Scripts\activate
# macOS / Linux için:
# source venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations users courses chatbot
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```
> `python manage.py seed_data` komutu 5 ekip üyesini (`20220236`, `20220194`, `20220404`, `20230147`, `20211046` — varsayılan şifre: `password123`), `SWE488` dahil örnek dersleri, vize/final sınav tarihlerini ve duyuruları otomatik oluşturur.

### B. Frontend (Next.js & Tailwind CSS) Kurulumu
```bash
cd frontend
npm install
npm run dev
```
Tarayıcıdan `http://localhost:3000/pages/login` adresine giderek giriş yapabilirsiniz.

### C. Test Senaryolarını (TC-01 .. TC-05) Otomatik Doğrulama
```bash
cd backend
python ../tests/run_test_cases.py
```

---

## 4. Herkesin GitHub'a Pushlaması İçin Adım Adım Rehber

Her ekip üyesi kendi görevini kendi branch'inde geliştirip GitHub'a pushlamak için şu komutları çalıştırır (detaylar [CONTRIBUTING.md](CONTRIBUTING.md) dosyasındadır):

```bash
# 1. Repoyu klonla
git clone https://github.com/ismailkaradayii/AI-Powered-University-Student-Assistant.git
cd AI-Powered-University-Student-Assistant

# 2. Kendi adına açılmış branch'e geç (Örnek: Barış için)
git checkout feature/baris-courses-exams

# 3. Kendi klasöründeki README_TASK.md dosyasını oku, geliştirmelerini yap ve kaydet
git add .
git commit -m "feat(courses): implement course and exam schedule endpoints for TC-03 and TC-05"

# 4. Kendi branch'ini GitHub'a pushla ve Pull Request (PR) aç
git push -u origin feature/baris-courses-exams
```
