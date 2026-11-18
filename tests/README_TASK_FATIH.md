# Görev Modülü 5: Live Chatbot UI, Admin Panel UI, QA Testing & Deployment
**Sorumlu:** Fatih Yazıcı (20211046)  
**İlgili WBS Maddeleri:** `4.2 (Live Chatbot UI Component & Integration)`, `5.1 (System Testing & <3s NFR Verification)`, `5.2 (Deployment: Vercel & Render/PythonAnywhere)`  
**İlgili Test Senaryoları:** `TC-03`, `TC-04`, `TC-05` (ve tüm `TC-01..TC-05` entegrasyon doğrulaması)  
**Branch:** `feature/fatih-chatbot-ui-admin-qa`

## Sorumluluk Alanın (`frontend/src/components/ChatbotWidget.jsx`, `frontend/src/pages/admin.js`, `tests/`)
1. **Canlı AI Chatbot Bileşeni (`ChatbotWidget.jsx`):**
   - Öğrenci panelinde sağ sütunda yer alan canlı sohbet penceresi.
   - `"When is the SWE488 midterm exam?"` (**TC-03**) ve `"What are the course add-drop rules?"` (**TC-04**) hızlı soru butonları, kaynak yönetmelik maddesi gösterimi (`citations`) ve `<3000ms` NFR yanıt süresi etiketi.
2. **Admin Panel Arayüzü (`admin.js` - `/pages/admin`):**
   - **TC-05:** Admin yetkisine sahip kullanıcının arayüz üzerinden yeni duyuru yayınlamasını ve sınav tarihini anında SQLite veritabanında güncellemesini sağlamak.
3. **Sistem Testleri ve Deployment (`tests/run_test_cases.py`, `tests/postman_collection.json`, `vercel.json`, `Procfile`):**
   - `TC-01` ile `TC-05` arasındaki tüm test senaryolarını otomatik doğrulayan Python test script'ini ve Postman koleksiyonunu çalıştırmak ve raporlamak.
   - Frontend (Vercel) ve Backend (Render/PythonAnywhere) canlı dağıtım yapılandırmalarını yönetmek.
