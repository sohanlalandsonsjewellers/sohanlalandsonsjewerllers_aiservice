# 🧠 Jewellery ERP — AI Service

**AI Service** ek independent microservice hai jo **Sohan Lal & Sons Jewellers ERP** ka brain hai. Ye service Analytics, Machine Learning based Forecasting/Recommendations, Business Intelligence, aur ek LLM-powered Business Advisor provide karti hai — sab kuch React Frontend + Express Backend se alag, apni khud ki FastAPI service ke through.

---

## 📌 Table of Contents

- [Monorepo Structure](#-project-structure-monorepo-level)
- [Environment Setup](#-environment-setup)
- [Folder Structure (Detailed)](#️-folder-structure--detailed-explanation)
- [Module Status](#-module-status)
- [Standard Workflow (API → DB)](#-standard-workflow-har-feature-ka-flow)
- [Code Likhne ka Order (Permanent Rule)](#-code-likhne-ka-order-permanent)
- [How to Add a New Module](#-naya-module-kaise-banaye)
- [Roadmap](#-roadmap)
- [Quick Start](#️-quick-start)

---

## 📁 Project Structure (Monorepo Level)

```
F:\SohanLalAndSonsJewellers\
│
├── backend       → Express.js API
├── frontend      → React App
└── ai-service    → FastAPI AI Service ✅ (is repo ka focus)
```

AI service, main backend aur frontend se **completely alag service** hai — independently develop, deploy aur scale hogi.

---

## ⚙️ Environment Setup

| Setup Item              | Status |
|--------------------------|--------|
| Python Installed          | ✅ |
| pip Installed              | ✅ |
| PATH Configured            | ✅ |
| VS Code Configured          | ✅ |
| Virtual Environment (`venv/`) | ✅ |
| MongoDB Connection (`DATABASE_URL`) | ✅ |
| FastAPI Server (`http://127.0.0.1:8001`) | ✅ |
| Health Check API (`GET /health`) | ✅ |

**Core Libraries Installed:**
- **FastAPI** — web framework
- **Motor** — async MongoDB driver
- **Pandas** — data processing
- **NumPy** — numerical computing
- **Scikit-learn** — machine learning
- **Pydantic** — data validation
- **Uvicorn** — ASGI server

**Health Check Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 🗂️ Folder Structure — Detailed Explanation

```
ai-service/
│
├── app/
│   ├── api/
│   │   ├── recommendation.py
│   │   ├── segmentation.py
│   │   ├── inventory.py
│   │   ├── demand.py
│   │   ├── sales.py
│   │   ├── revenue.py
│   │   ├── business_summary.py
│   │   ├── reorder.py
│   │   ├── performance.py
│   │   ├── report.py
│   │   ├── festival.py
│   │   ├── clv.py
│   │   ├── churn.py
│   │   ├── pricing.py
│   │   └── dashboard.py
│   │
│   ├── services/
│   │   ├── recommendation_service.py
│   │   ├── segmentation_service.py
│   │   ├── inventory_service.py
│   │   ├── demand_service.py
│   │   ├── sales_service.py
│   │   ├── revenue_service.py
│   │   ├── business_summary_service.py
│   │   ├── reorder_service.py
│   │   ├── performance_service.py
│   │   ├── report_service.py
│   │   ├── festival_service.py
│   │   ├── clv_service.py
│   │   ├── churn_service.py
│   │   ├── pricing_service.py
│   │   └── dashboard_service.py
│   │
│   └── ml/
│       ├── recommendationModel/
│       ├── demandForecastModel/
│       ├── salesForecastModel/
│       ├── businessSummaryModel/
│       │   ├── business_score.py
│       │   ├── inventory_health.py
│       │   ├── sales_health.py
│       │   ├── customer_health.py
│       │   ├── alert_engine.py
│       │   └── recommendation_engine.py
│       ├── reorderModel/
│       ├── performanceModel/
│       ├── customerModel/
│       │   ├── clv_model.py
│       │   └── churn_model.py
│       ├── festivalModel/
│       │   └── festival_predictor.py
│       ├── pricingModel/
│       └── reportModel/
│
├── models/              # Pydantic models (request/response validation)
├── routes/              # (legacy/alias — prefer app/api/)
├── utils/               # Helper / reusable functions
│
├── database.py          # MongoDB connection setup
├── main.py               # App entry point
├── config.py             # Configuration & settings
├── __init__.py
│
├── .env                  # Secrets (never commit)
├── requirements.txt       # Python dependencies
└── venv/                  # Virtual environment
```

### Key Files

| File / Folder     | Purpose |
|--------------------|---------|
| `app/api/`          | HTTP endpoints only — no business logic here |
| `app/services/`      | Orchestration layer — calls DB + ML models, builds response |
| `app/ml/`            | Actual ML/business logic, isolated per module |
| `database.py`        | Single source of truth for MongoDB connection |
| `main.py`            | Entry point — starts the FastAPI server |
| `config.py`          | `PORT`, `DATABASE_URL`, API keys (Gemini/OpenAI/DeepSeek/Ollama — future), model settings |
| `.env`               | Secrets — never commit, must be in `.gitignore` |
| `requirements.txt`    | Python dependency manifest (equivalent to `package.json`) |
| `models/`            | Pydantic schemas: `Customer`, `Order`, `Revenue`, `Prediction`, `Recommendation` |
| `utils/`             | Date formatting, currency formatting, math helpers, common utilities |

---

## ✅ Module Status

### Completed Modules (16)

| # | Module | Endpoint | Key Features |
|---|--------|----------|---------------|
| 1 | AI Recommendation Engine | `/ai/recommend/{productId}` | Content-based recommendation, cosine similarity, similar products, score, category matching |
| 2 | Customer Segmentation | `/ai/customer-segmentation` | VIP, Premium, Regular, New Customer |
| 3 | Inventory Intelligence | `/ai/inventory` | Low stock, healthy stock, fast moving, dead stock, recommendation |
| 4 | Demand Forecast | `/ai/demand-forecast` | Model selector, daily forecast, history, product-wise forecast |
| 5 | Demand Insights | `/ai/demand-insights` | Stock risk, trend, coverage, demand score, recommendation |
| 6 | Revenue Forecast | `/ai/revenue` | Revenue prediction |
| 7 | Sales Forecast | `/ai/sales-forecast` | Revenue history, forecast, model selection |
| 8 | Sales History | `/ai/sales-history` | Historical sales data |
| 9 | Sales Summary | `/ai/sales-summary` | Aggregated sales summary |
| 10 | Business Summary | `/ai/business-summary` | Business score, inventory/sales/customer health, alerts, recommendations |
| 11 | Business Score Engine | *(internal)* | Weighted score, grade, breakdown |
| 12 | Inventory Health Engine | *(internal)* | Excellent, Healthy, Average, Critical |
| 13 | Sales Health Engine | *(internal)* | Growing, Stable, Excellent |
| 14 | Customer Health Engine | *(internal)* | VIP, Premium, Regular, New |
| 15 | Alert Engine | *(internal)* | Low stock, pending order, out of stock |
| 16 | Recommendation Engine (Business Summary) | *(internal)* | Restock, promotion, inventory suggestion |

### Remaining Modules (Priority Order)

| # | Module | Endpoint | Priority | What it Needs to Do |
|---|--------|----------|----------|----------------------|
| 1 | Smart Reorder Engine | `/ai/reorder-plan` | ⭐⭐⭐⭐⭐ | Calculate `recommendedQty` per product based on current stock + velocity. Output: `{ "product": "Ring", "currentStock": 2, "recommendedQty": 15, "reason": "Fast Moving" }` |
| 2 | Product Performance Analytics | `/ai/product-performance` | ⭐⭐⭐⭐⭐ | Classify products: Best Seller, Slow Seller, Dead Stock, Profit Potential |
| 3 | AI Report Generator | `/ai/report` | ⭐⭐⭐⭐⭐ | Generate PDF / Excel owner reports from aggregated business data |
| 4 | Customer Lifetime Value (CLV) | `/ai/customer-clv` | ⭐⭐⭐⭐ | Predict long-term value per customer from order history |
| 5 | Customer Churn Prediction | `/ai/customer-churn` | ⭐⭐⭐⭐ | Identify customers likely to stop purchasing |
| 6 | Festival Demand Prediction | `/ai/festival-demand` | ⭐⭐⭐⭐ | Forecast demand spikes for Diwali, Wedding Season, Raksha Bandhan, etc. |
| 7 | Dynamic Pricing Suggestions | `/ai/pricing` | ⭐⭐⭐ | Suggest price adjustments based on demand/stock/competition signals |
| 8 | Executive Dashboard Summary | `/ai/dashboard` | ⭐⭐⭐ | Single API aggregating all module outputs for a dashboard view |

### 🏆 Overall Project Completion

| Layer | Progress |
|-------|----------|
| Core AI Backend | ≈ 75% `█████████████████████░░░░░░░` |
| Business Intelligence | ≈ 85% `███████████████████████░░░░░` |
| AI + ML Architecture | ≈ 90% `█████████████████████████░░░` |

**Final Roadmap Order:**
1. Smart Reorder Engine
2. Product Performance Analytics
3. Customer Lifetime Value (CLV)
4. Customer Churn Prediction
5. Festival Demand Prediction
6. AI Report Generator (PDF + Excel)
7. Executive Dashboard API

Is roadmap ke baad ye AI service sirf ek demo project nahi rahega, balki jewellery e-commerce ke liye ek **production-ready Business Intelligence & Decision Support backend** ban jayega.

---

## 🔁 Standard Workflow (Har Feature ka Flow)

Har feature isi pattern ko follow karta hai:

```
API
 ↓
Service
 ↓
ML Model(s)
 ↓
Database
 ↓
Response (JSON)
```

**Example — Business Summary:**

```
GET /ai/business-summary
        ↓
BusinessSummaryService
        ↓
   ┌────────────────────┐
   │ BusinessScoreModel   │
   │ InventoryHealthModel │
   │ SalesHealthModel     │
   │ CustomerHealthModel  │
   │ AlertEngine          │
   │ RecommendationEngine │
   └────────────────────┘
        ↓
     MongoDB
        ↓
      JSON
```

**Example — Recommendation:**
```
API → RecommendationService → SimilarityModel → MongoDB → JSON
```

**Example — Demand:**
```
API → DemandService → ModelSelector → (Linear | RandomForest) → MongoDB → JSON
```

**Example — Sales:**
```
API → SalesService → ModelSelector → ForecastModel → MongoDB → JSON
```

**Example — Inventory:**
```
API → InventoryService → InventoryModel → DemandModel → MongoDB → JSON
```

---

## 🧩 Code Likhne ka Order (Permanent)

Naya module banate waqt, is exact order me code likho:

| Step | Task |
|------|------|
| 1 | **API define karo** — route + HTTP method (`GET`/`POST`/`PUT`) |
| 2 | **Service banao** — sirf orchestration, koi heavy logic nahi |
| 3 | **Database Query** — orders, products, users fetch karo |
| 4 | **Data Cleaning** — raw data ko usable format me convert karo |
| 5 | **Feature Engineering** — model ke liye required features banao |
| 6 | **Model Selection** — kaunsa ML model use karna hai decide karo |
| 7 | **ML Model** — actual prediction/calculation logic |
| 8 | **Business Logic** — domain rules apply karo (thresholds, grading, etc.) |
| 9 | **JSON Response** — final structured output return karo |
| 10 | **Testing** — unit + integration test |
| 11 | **Integration with Frontend** — React se connect karo |

### Minimal Code Skeleton

```python
# app/api/business_summary.py
from fastapi import APIRouter
from app.services.business_summary_service import BusinessSummaryService

router = APIRouter()

@router.get("/ai/business-summary")
async def get_business_summary():
    return await BusinessSummaryService.summary()
```

```python
# app/services/business_summary_service.py
from app.ml.businessSummaryModel.inventory_health import InventoryHealthModel
from app.ml.businessSummaryModel.sales_health import SalesHealthModel
from app.ml.businessSummaryModel.customer_health import CustomerHealthModel
from app.ml.businessSummaryModel.business_score import BusinessScoreModel

class BusinessSummaryService:
    @staticmethod
    async def summary():
        # Step 1: fetch data
        orders = await get_orders()
        products = await get_products()
        customers = await get_customers()

        # Step 2: run models
        inventory = InventoryHealthModel.calculate(products)
        sales = SalesHealthModel.calculate(orders)
        customer = CustomerHealthModel.calculate(customers)
        score = BusinessScoreModel.calculate(inventory, sales, customer)

        # Step 3: build response
        return {
            "business_score": score,
            "inventory_health": inventory,
            "sales_health": sales,
            "customer_health": customer
        }
```

```python
# app/ml/businessSummaryModel/inventory_health.py
class InventoryHealthModel:
    @staticmethod
    def calculate(products):
        # domain logic here — Excellent / Healthy / Average / Critical
        ...
        return {"status": "Healthy", "score": 82}
```

**Final Rule:** Har feature ka pattern same rahega — `API → Service → Model → Database → Response`. Agar ek module me multiple ML logic ho, to:

```
API → Service → [Model 1, Model 2, Model 3, Model 4] → Database → JSON
```

---

## ➕ Naya Module Kaise Banaye

Sirf 3 naye files banao — kahin aur kuch touch nahi:

**Example — Customer Churn:**
```
app/api/churn.py
        ↓
app/services/churn_service.py
        ↓
app/ml/customerModel/churn_model.py
        ↓
     MongoDB
        ↓
    Response
```

**Example — Festival Prediction:**
```
app/api/festival.py → app/services/festival_service.py → app/ml/festivalModel/festival_predictor.py
```

**Example — CLV:**
```
app/api/clv.py → app/services/clv_service.py → app/ml/customerModel/clv_model.py
```

> Existing code kabhi rewrite nahi karna padta — sirf naya module add hota hai.

---

## 🚀 Roadmap

### Phase 1 — Analytics APIs
- [x] Sales Summary
- [x] Revenue Summary
- [x] Product Analytics (partial — Inventory Intelligence)
- [x] Customer Analytics (Segmentation)
- [ ] Full Dashboard API

### Phase 2 — Machine Learning
- [x] Sales Forecasting
- [x] Customer Segmentation
- [x] Product Recommendation
- [x] Demand Prediction
- [ ] Smart Reorder Engine
- [ ] Product Performance Analytics
- [ ] Customer Lifetime Value (CLV)
- [ ] Customer Churn Prediction
- [ ] Festival Demand Prediction
- [ ] Dynamic Pricing

### Phase 3 — LLM Integration
- [ ] AI Business Advisor

**Example Output:**
> "Pichhle 30 din me revenue 15% bada hai. Silver category ki sales kam hui hai. Raksha Bandhan se pehle silver anklets aur bangles ka stock badhana faydemand ho sakta hai."

### Phase 4 — Reporting
- [ ] AI Report Generator (PDF + Excel)
- [ ] Executive Dashboard Summary

---

## 🎯 Final Goal

| Layer            | Technology                    |
|-------------------|--------------------------------|
| Frontend          | React                           |
| Backend           | Express                          |
| Database          | MongoDB                          |
| AI Service        | FastAPI                          |
| Machine Learning   | Forecasting & Recommendations     |
| Intelligence      | LLM-based Business Advisor        |

Project complete hone ke baad, ye sirf ek e-commerce website nahi, balki ek **AI-powered Jewellery ERP** hoga.

---

## 🏗️ Architecture Principles

- **Modular microservice architecture** — AI service backend/frontend se completely independent.
- Har feature **isolated** rehta hai (apna API + Service + Model).
- **Service layer sirf orchestration** karta hai — koi heavy computation nahi.
- **ML logic sirf `ml/` models me** rehta hai.
- **API bahut clean** rehti hai — sirf request/response handling.
- Future modules (CLV, Churn, Festival Prediction, Smart Pricing, Reorder, AI Reports) add karne ke liye sirf **naya module banana padta hai** — existing code touch nahi hota.

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

---

## 📄 License

Internal project — Sohan Lal & Sons Jewellers. Not for public distribution.
