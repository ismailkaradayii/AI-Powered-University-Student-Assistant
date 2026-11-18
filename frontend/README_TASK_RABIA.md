# Görev Modülü 4: Frontend UI Architecture, Login & Student Dashboard
**Sorumlu:** Rabia Basan (20230147)  
**İlgili WBS Maddeleri:** `3.1 (UI/UX Prototyping & Next.js Tailwind Setup)`, `3.2 (Frontend Login Page & Dashboard Page)`  
**İlgili Test Senaryoları:** `TC-01 (Student Secure Login)`, `TC-02 (Login with Incorrect Password)`  
**Branch:** `feature/rabia-frontend-auth-dashboard`

## Sorumluluk Alanın (`frontend/src/pages/login.js`, `frontend/src/pages/dashboard.js`, `frontend/src/components/Layout.jsx`, `frontend/src/lib/api.js`)
1. **Tasarım Sistemi ve Layout (`Layout.jsx`, `api.js`):**
   - Next.js + Tailwind CSS ile mobil ve masaüstü uyumlu (responsive) üniversite öğrenci portalı üst menüsü (Navbar), oturum yönetimi ve JWT token saklama fonksiyonları.
2. **Öğrenci Giriş Sayfası (`login.js` - `/pages/login`):**
   - **TC-01:** Öğrenci numarası ve şifre formu doldurulup "Login" butonuna basıldığında JWT token'ı kaydetmek ve kullanıcıyı `/pages/dashboard` sayfasına yönlendirmek.
   - **TC-02:** Hatalı şifre girildiğinde sunucudan dönen HTTP 401 hatasını yakalayıp ekranda kırmızı bilgilendirici hata kutusu (`role="alert"`) göstermek.
3. **Öğrenci Paneli (`dashboard.js` - `/pages/dashboard`):**
   - Haftalık ders programı tablosu (`Course` listesi), sınav takvimi kartları (`Exam` listesi) ve güncel duyuruları (`Announcement` listesi) Backend API'den çekerek ekranda göstermek.
