# Görev Modülü 2: Course, Exam & Announcement Management System
**Sorumlu:** Barış Avanoğlu (20220194)  
**İlgili WBS Maddeleri:** `2.1 (Courses, Exams, Announcements)`, `2.3`  
**İlgili Test Senaryoları:** `TC-03 (Course & Exam Info Query DB)`, `TC-05 (Admin Panel Data Update)`  
**Branch:** `feature/baris-courses-exams`

## Sorumluluk Alanın (`backend/apps/courses/`)
1. **Veritabanı Modelleri ve Şema (`models.py`):**
   - `Course`: Ders kodu (`SWE488`), adı, öğretim üyesi, gün, başlangıç/bitiş saati ve derslik bilgileri.
   - `Exam`: Derse bağlı (`ForeignKey`) sınav türü (`Midterm`, `Final`), sınav tarihi, saati ve sınav salonu.
   - `Announcement`: Duyuru başlığı, içeriği, önem durumu (`is_important`) ve oluşturulma tarihi.
2. **REST API Endpoint'leri (`views.py`, `serializers.py`, `urls.py`):**
   - `GET /api/courses/`, `GET /api/exams/`, `GET /api/announcements/` ile öğrenci paneline (Dashboard) veri sağlamak.
   - `IsAdminOrReadOnly` yetki kontrolü ile yalnızca Admin kullanıcıların yeni duyuru eklemesini ve sınav tarihi güncellemesini sağlamak (**TC-05**).
   - Ders koduna göre filtreleme (`?code=SWE488`) desteğini geliştirmek.
3. **Veritabanı Başlangıç Verileri (`management/commands/seed_data.py`) & Testler (`tests.py`):**
   - `python manage.py seed_data` komutu ile örnek dersleri, sınavları ve duyuruları oluşturmak.
   - `tests.py` içerisine `TC-05` senaryosunu (Admin tarafından sınav tarihi ve duyuru güncellenmesi) test eden birim testlerini eklemek.
