# Görev Modülü 3: AI Chatbot & RAG Engine Implementation
**Sorumlu:** Mustafa Özgür Güdükboy (20220404)  
**İlgili WBS Maddeleri:** `4.1 (RAG Mechanism & Regulations KB Integration)`, `5.1 (<3s NFR Performance Tuning)`  
**İlgili Test Senaryoları:** `TC-03 (Course & Exam Info Query)`, `TC-04 (Regulation Knowledge Base Query - RAG)`  
**İlgili Riskler:** `R1 (<3 saniye NFR hedefi)`, `R2 (Hallucination önleme - Strict Context Prompting)`  
**Branch:** `feature/mustafa-ai-rag-chatbot`

## Sorumluluk Alanın (`backend/apps/chatbot/` ve `backend/data/regulations/`)
1. **RAG Mekanizması ve Yönetmelik Bilgi Tabanı (`rag_engine.py`):**
   - `backend/data/regulations/` içindeki üniversite yönetmelik metinlerini/PDF'lerini indekslemek ve semantik arama ile en alakalı yönetmelik maddesini (`Article 14 - Add-Drop Rules`, `Article 15 - Withdrawal`, `Article 18 - Attendance` vb.) bulmak.
   - **Risk R2 Çözümü (Strict Context Prompting):** Yapay zekanın uydurma (hallucination) bilgi üretmesini engellemek için yalnızca yönetmelik metnine sadık kalan ve madde numarasını kaynak gösteren prompt mimarisini uygulamak (**TC-04**).
2. **Hibrit Sorgu Yönlendirici ve <3 Saniye NFR Optimizasyonu (`services.py`):**
   - `"When is the SWE488 midterm exam?"` gibi ders/sınav sorularında ders kodunu (`SWE488`) algılayıp SQLite veritabanından milisaniyeler içinde sınav tarihini ve dersliği getirmek (**TC-03** ve **Risk R1**).
   - Yönetmelik sorularını (`"What are the course add-drop rules?"`) RAG motoruna yönlendirmek (**TC-04**).
3. **Chatbot API & Performans Loglama (`views.py`, `models.py`):**
   - `POST /api/chatbot/ask/` endpoint'i üzerinden cevabı, kaynak tipini (`DATABASE` veya `RAG`), ilgili madde kaynaklarını (`citations`) ve yanıt süresini (`response_time_ms`) döndürmek.
