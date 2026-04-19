# 🤖 GPREC IntelliBot

**AI-Powered Navigator and Information Hub for Students**  
G. Pulla Reddy Engineering College (Autonomous), Kurnool  
Batch: CSE-A7 | Project Date: 14/7/2025

---

## 🚀 Quick Start (Windows)

**Option 1 — One click:**
```
Double-click START_APP.bat
```

**Option 2 — Manual:**
```bash
# Terminal 1 - Backend
pip install -r requirements.txt
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
streamlit run app.py --server.port 8501
```

Open: **http://localhost:8501**  
API Docs: **http://localhost:8000/docs**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 AI Chat | Gemini-powered chatbot with conversation history |
| 🗺️ Campus Map | Visual campus navigation with 15+ locations |
| 💼 Placement Analyzer | Company eligibility checker + AI career advice |
| 📢 Notifications | Real-time campus announcements with filters |
| 🌐 Multilingual | English, Telugu (తెలుగు), Hindi (हिंदी) |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit 1.39
- **Backend:** FastAPI 0.115 + Python 3.10+
- **AI:** Google Gemini 1.5 Flash
- **Database:** SQLite + SQLAlchemy
- **Server:** Uvicorn

---

## 🧪 Testing

```bash
pytest tests/ -v
# Expected: 40 tests passed
```

---

## 👥 Team

| Name | Roll No | Role |
|------|---------|------|
| G. Sindhuja | 229X1A05E1 | AI/NLP Integration |
| R. Anjali Devi | 239X5A05M0 | Frontend & Notifications |
| A. Sucharitha Devi | 229X1A0567 | Backend & Placement |

**Guide:** D.L.N Prasunna, Assistant Professor

---

## 📁 Project Structure

```
gprec_intellibot/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings + campus data
│   ├── database.py          # SQLAlchemy models
│   ├── gemini_service.py    # Gemini AI integration
│   └── routers/
│       ├── chat.py          # Chat endpoints
│       ├── placement.py     # Placement endpoints
│       ├── notifications.py # Notification endpoints
│       └── campus.py        # Campus map endpoints
├── frontend/
│   └── app.py               # Streamlit UI
├── tests/
│   └── test_intellibot.py   # 40+ test cases
├── docs/
│   └── GPREC_IntelliBot_Documentation.docx
├── requirements.txt
├── START_APP.bat            # One-click launcher
├── start_backend.bat
└── start_frontend.bat
```
