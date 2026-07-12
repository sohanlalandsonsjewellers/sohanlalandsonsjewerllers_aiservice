# 🧠 Jewellery ERP — AI Service

**AI Service** ek independent microservice hai jo future me **Sohan Lal & Sons Jewellers ERP** ka brain banegi. Ye service Analytics, Machine Learning based Forecasting/Recommendations, aur ek LLM-powered Business Advisor provide karegi — sab kuch React Frontend + Express Backend se alag, apni khud ki FastAPI service ke through.

---

## 📁 Project Structure (Monorepo Level)

```
F:\SohanLalAndSonsJewellers\
│
├── backend       → Express.js API
├── frontend      → React App
└── ai-service    → FastAPI AI Service ✅ (is repo ka focus)
```

AI backend, main backend aur frontend se **completely alag service** hai — independently develop, deploy aur scale hogi.

---

## ✅ Ab Tak Kya Complete Hua

### 1. AI Service Project Setup
`ai-service/` folder alag standalone service ke roop me create ho chuka hai.

### 2. Python Environment
- ✅ Python Installed
- ✅ pip Installed
- ✅ PATH Configured
- ✅ VS Code Configured

### 3. Virtual Environment (`venv/`)
Har project ke dependencies isolated rehte hain, taaki conflicts na ho:

| Service  | Isolation           |
|----------|---------------------|
| Backend  | Node Modules         |
| AI       | Python `venv`         |

Dono ek dusre se independent hai — koi package clash nahi hoga.

### 4. Core Libraries Installed
- **FastAPI** — web framework
- **Motor** — async MongoDB driver
- **Pandas** — data processing
- **NumPy** — numerical computing
- **Scikit-learn** — machine learning
- **Pydantic** — data validation
- **Uvicorn** — ASGI server

### 5. MongoDB Connection
`DATABASE_URL` ke through AI Service ab tumhare existing **Jewellery Database** se directly connect ho sakti hai.

### 6. FastAPI Server Running
```
http://127.0.0.1:8001
```

### 7. Health Check API
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

Matlab: `AI Service → MongoDB` connection successfully establish ho chuka hai.

---

## 🗂️ Folder Structure — Detailed Explanation

```
ai-service/
│
├── app/                # Core AI application code
│
├── models/             # Pydantic models (data validation)
│
├── routes/             # API endpoints
│
├── services/           # Business logic layer
│
├── utils/              # Helper / reusable functions
│
├── database.py         # MongoDB connection setup
├── main.py              # App entry point
├── config.py            # Configuration & settings
├── __init__.py
│
├── .env                 # Secrets (never commit)
├── requirements.txt      # Python dependencies
└── venv/                 # Virtual environment
```

### `app/`
Poora AI application yahin exist karta hai — jo bhi actual functional code hoga, wo is folder ke andar organize hoga.

### `database.py`
MongoDB connection ka single source of truth. Yahin se poori project (Orders, Products, Customers, Bills, Analytics) database ko read/query karegi.

### `main.py`
AI Service ka **entry point** — jaise Node.js me `server.ts` hota hai, waise hi Python me `main.py` server ko start karta hai.

### `config.py`
Saari configuration values ek jagah:
- `PORT`
- `DATABASE_URL`
- API Keys
- Model Settings

Future me isi file me add honge:
- `Gemini Key`
- `OpenAI Key`
- `DeepSeek`
- `Ollama`

### `.env`
Saare **secrets** yahan store hote hain — `DATABASE_URL`, API Keys, Passwords, Tokens. Ye file **kabhi bhi GitHub par upload nahi hoti** (`.gitignore` me hona chahiye).

### `requirements.txt`
Python ka dependency manifest — Node.js ke `package.json` ka equivalent.

### `routes/`
Saare API endpoints yahan define hote hain:
- `analytics.py`
- `prediction.py`
- `recommendation.py`
- `chat.py`
- `dashboard.py`

Har route sirf HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) handle karta hai — actual logic nahi.

### `services/`
Yahan **actual business logic** hota hai. Ye clean architecture ka core principle hai — routes sirf request receive karte hain, calculation `services/` layer karta hai.

**Example:**
- Route `GET /analytics` → sirf request receive karta hai
- Service layer calculate karta hai: `Revenue`, `Top Products`, `Sales Growth`, `Forecast`

### `models/`
Pydantic models jo data validation define karte hain:
- `Customer`
- `Order`
- `Revenue`
- `Prediction`
- `Recommendation`

### `utils/`
Reusable helper functions jo baar-baar use hote hain:
- Date Formatting
- Currency Formatting
- ML Helper Functions
- Math Utilities
- Common Utilities

### `venv/`
Python virtual environment — **manually edit nahi karte**.

---

## 🚀 Roadmap — Aage Kya Banega

### Phase 1 — Analytics APIs
- [ ] Sales Summary
- [ ] Revenue Summary
- [ ] Product Analytics
- [ ] Customer Analytics
- [ ] Dashboard APIs

### Phase 2 — Machine Learning
- [ ] Sales Forecasting
- [ ] Customer Segmentation
- [ ] Product Recommendation
- [ ] Demand Prediction

### Phase 3 — LLM Integration
- [ ] AI Business Advisor

**Example Output:**
> "Pichhle 30 din me revenue 15% bada hai. Silver category ki sales kam hui hai. Raksha Bandhan se pehle silver anklets aur bangles ka stock badhana faydemand ho sakta hai."

---

## 🎯 Final Goal

Project complete hone ke baad, ye sirf ek e-commerce website nahi, balki ek **AI-powered Jewellery ERP** hoga jisme ye sab components saath me kaam karenge:

| Layer            | Technology                          |
|------------------|--------------------------------------|
| Frontend         | React                                |
| Backend          | Express                              |
| Database         | MongoDB                              |
| AI Service       | FastAPI                              |
| Machine Learning | Forecasting & Recommendations        |
| Intelligence     | LLM-based Business Advisor           |

---

## 🏗️ Architecture Recommendation

Is project ko **modular microservice architecture** me hi rakha jaana chahiye. Isse future me:
- AI Models
- Recommendation Engine
- Chat Assistant
- Forecasting Engine

...sab **independently scale aur maintain** kiye ja sakenge, bina backend/frontend ko touch kiye.

---

## 🛠️ Quick Start

```bash
# 1. Navigate to ai-service folder
cd ai-service

# 2. Activate virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload --port 8001
```

Server chalne ke baad check karo:
```
http://127.0.0.1:8001/health
```
