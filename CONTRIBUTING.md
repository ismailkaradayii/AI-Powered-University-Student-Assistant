# Ekip Üyeleri İçin Git & GitHub Çalışma Rehberi (SWE488)

Bu rehber, 5 ekip üyesinin hiçbir çakışma (*merge conflict*) yaşamadan kendi görevlerini geliştirip GitHub'a pushlaması için hazırlanmıştır.

---

## Kişiye Özel Branch ve Klasör Haritası

1. **İsmail Karadayı (`20220236`)**
   - **Branch:** `feature/ismail-auth-users`
   - **Çalışacağı Klasör:** `backend/apps/users/`
   - **Görev Özeti:** `backend/apps/users/README_TASK.md`

2. **Barış Avanoğlu (`20220194`)**
   - **Branch:** `feature/baris-courses-exams`
   - **Çalışacağı Klasör:** `backend/apps/courses/`
   - **Görev Özeti:** `backend/apps/courses/README_TASK.md`

3. **Mustafa Özgür Güdükboy (`20220404`)**
   - **Branch:** `feature/mustafa-ai-rag-chatbot`
   - **Çalışacağı Klasör:** `backend/apps/chatbot/` ve `backend/data/regulations/`
   - **Görev Özeti:** `backend/apps/chatbot/README_TASK.md`

4. **Rabia Basan (`20230147`)**
   - **Branch:** `feature/rabia-frontend-auth-dashboard`
   - **Çalışacağı Klasör:** `frontend/src/pages/login.js`, `frontend/src/pages/dashboard.js`, `frontend/src/components/Layout.jsx`, `frontend/src/lib/api.js`
   - **Görev Özeti:** `frontend/README_TASK_RABIA.md`

5. **Fatih Yazıcı (`20211046`)**
   - **Branch:** `feature/fatih-chatbot-ui-admin-qa`
   - **Çalışacağı Klasör:** `frontend/src/components/ChatbotWidget.jsx`, `frontend/src/pages/admin.js`, `tests/`
   - **Görev Özeti:** `tests/README_TASK_FATIH.md`

---

## Herkesin Sırasıyla Uygulayacağı Git Komutları

### 1. Projeyi Bilgisayarına İndir
```bash
git clone https://github.com/ismailkaradayii/AI-Powered-University-Student-Assistant.git
cd AI-Powered-University-Student-Assistant
```

### 2. Kendi Branch'ine Geç
Branch'ler GitHub üzerinde hazır olarak açılmıştır. Kendi ismine ait komutu çalıştır:
- **İsmail:** `git checkout feature/ismail-auth-users`
- **Barış:** `git checkout feature/baris-courses-exams`
- **Mustafa Özgür:** `git checkout feature/mustafa-ai-rag-chatbot`
- **Rabia:** `git checkout feature/rabia-frontend-auth-dashboard`
- **Fatih:** `git checkout feature/fatih-chatbot-ui-admin-qa`

### 3. Geliştirmeni Yap, Commit At ve Pushla
Kendi klasöründeki geliştirmeleri, testleri ve iyileştirmeleri tamamladıktan sonra:
```bash
git status
git add .
git commit -m "feat: complete assigned WBS module and test cases"
git push origin HEAD
```

### 4. GitHub Üzerinden Pull Request (PR) Aç
GitHub repo sayfasına girdiğinde üstte çıkan **"Compare & pull request"** butonuna tıklayarak kendi branch'ini `main` branch'ine birleştir (Merge). Böylece GitHub *Contributors* ve *Commits* geçmişinde 5 kişinin tamamının katkısı net ve eşit şekilde görünecektir.
