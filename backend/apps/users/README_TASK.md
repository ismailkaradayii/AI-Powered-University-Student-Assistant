# Görev Modülü 1: Student Authentication, JWT & Admin Permissions
**Sorumlu:** İsmail Karadayı (20220236)  
**İlgili WBS Maddeleri:** `1.2`, `2.1 (Users)`, `2.2`  
**İlgili Test Senaryoları:** `TC-01 (Student Secure Login)`, `TC-02 (Login with Incorrect Password)`  
**Branch:** `feature/ismail-auth-users`

## Tamamlanan Özellikler (`backend/apps/users/`)
1. **Custom Student User Modeli (`models.py`):**
   - `student_number` tabanlı benzersiz kimlik doğrulama, güvenli şifre hashleme, `role` (`admin`/`student`) özelliği ve `created_at`/`updated_at` zaman damgaları.
2. **JWT Authentication, Kayıt & Profil API'leri (`views.py`, `serializers.py`, `urls.py`, `permissions.py`):**
   - `POST /api/auth/login/`: Geçerli kimlik bilgileriyle HTTP `200 OK` ve JWT (`access`, `refresh`) üretir (**TC-01**); hatalı şifre veya tanımsız öğrenci numarasında HTTP `401 Unauthorized` döner (**TC-02**); pasif hesaplarda HTTP `403 Forbidden` döner.
   - `POST /api/auth/register/`: Yeni öğrenci kaydı, şifre uzunluğu/eşleşme doğrulaması ve otomatik JWT token üretimi.
   - `POST /api/auth/refresh/`: Süresi dolan access token'ı yenileme.
   - `GET / PATCH /api/auth/me/`: Giriş yapan öğrencinin profilini görüntüleme ve yetki yükseltmeye kapalı güvenli profil güncelleme.
   - `POST /api/auth/change-password/`: Eski şifre doğrulamalı güvenli şifre değiştirme.
   - `GET /api/auth/admin/students/` ve `GET / PATCH /api/auth/admin/students/<id>/`: Yalnızca Admin (`IsAdminStudent`) kullanıcıların öğrenci yetkilerini (`is_staff`, `is_active`) yönetmesi.
3. **Django Admin & Otomatik Birim Testleri (`admin.py`, `tests.py`):**
   - Toplu hesap aktifleştirme/pasifleştirme ve admin yetkisi verme aksiyonları (`StudentUserAdmin`).
   - `TC-01`, `TC-02`, kayıt, profil, şifre değiştirme, token yenileme ve admin yetki kontrolünü doğrulayan 11 adet `APITestCase` birim testi (`python manage.py test apps.users`).
