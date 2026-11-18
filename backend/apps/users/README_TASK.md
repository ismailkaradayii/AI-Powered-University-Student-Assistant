# Görev Modülü 1: Student Authentication, JWT & Admin Permissions
**Sorumlu:** İsmail Karadayı (20220236)  
**İlgili WBS Maddeleri:** `1.2`, `2.1 (Users)`, `2.2`  
**İlgili Test Senaryoları:** `TC-01 (Student Secure Login)`, `TC-02 (Login with Incorrect Password)`  
**Branch:** `feature/ismail-auth-users`

## Sorumluluk Alanın (`backend/apps/users/`)
1. **Custom Student User Modeli (`models.py`):**
   - `student_number` ile giriş yapılabilen, şifreleri güvenli şekilde hashleyen (`PBKDF2/Argon2`) özel kullanıcı modeli.
2. **JWT Authentication & Login API (`views.py`, `serializers.py`, `urls.py`):**
   - `POST /api/auth/login/`: Doğru öğrenci numarası ve şifre girildiğinde JWT (`access` ve `refresh`) token ve kullanıcı profilini döner (**TC-01**).
   - Yanlış şifre girildiğinde HTTP `401 Unauthorized` ve anlamlı hata mesajı döner (**TC-02**).
   - `GET /api/auth/me/`: Giriş yapan öğrencinin profil ve yetki (`is_staff`) bilgilerini döner.
3. **Django Admin Kullanıcı Yönetimi (`admin.py`) & Unit Testler (`tests.py`):**
   - `tests.py` içerisine `TC-01` ve `TC-02` senaryolarını doğrulayan Django APITestCase testlerini eklemek/geliştirmek.
   - Şifre değiştirme veya yeni öğrenci kaydı (`/api/auth/register/`) endpoint'ini tamamlamak.
