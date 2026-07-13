# BankGuard Enterprise 🛡️

> **Finspark '26 Hackathon** — AI-Powered Behavioral Threat & Fraud Detection for Banking

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal.svg)](https://fastapi.tiangolo.com)

---

## 🚨 The Problem

Indian banks lose **₹100+ Crores annually** to insider fraud. The PNB-Nirav Modi scam (₹11,400 Cr) exploited a gap between SWIFT messages and CBS records — a gap that went undetected for **7 years**.

## 💡 Our Solution

**BankGuard Enterprise** is a real-time, AI-powered fraud detection platform that correlates risk signals across **5 independent analytics modules** to catch coordinated fraud — the kind that single-module systems miss.

### Six-Module Architecture

| # | Module | Algorithm | Risk Weight |
|---|--------|-----------|-------------|
| 1 | **UEBA** (Behavior) | Isolation Forest + Peer Groups | 0–20 pts |
| 2 | **Loan Intelligence** | XGBoost + SHAP | 0–30 pts |
| 3 | **Compliance Engine** | SWIFT/CBS Reconciler + JSON Rules | 0–45 pts |
| 4 | **NLP Analyzer** | Sentence Transformers + Intent | 0–10 pts |
| 5 | **Graph Analytics** | Neo4j + Louvain + Centrality | 0–15 pts |
| 6 | **Meta Risk Engine** | Cross-Signal Correlator | → 0–100 |

> **Key Insight:** 3 medium signals pointing at the **same person** trigger a CRITICAL alert — catching coordinated fraud that isolated systems miss entirely.

---

## 📁 Project Structure

```
finsparkk-26/
├── plan.md                                # Full project plan & roadmap
├── docs/
│   ├── system-architecture-diagrams.html  # 10 interactive SVG diagrams
│   └── bankguard-architecture.svg         # System architecture overview
├── frontend/                              # Dashboard UI
│   ├── index.html                         # Main dashboard
│   ├── css/styles.css                     # Dark-theme design system
│   ├── js/app.js                          # Dashboard logic & charts
│   └── assets/                            # Static assets
├── backend/                               # FastAPI REST API
│   ├── main.py                            # App entry point
│   ├── config.py                          # Environment config
│   ├── requirements.txt                   # Python dependencies
│   ├── models/                            # SQLAlchemy + Pydantic models
│   ├── routes/                            # API endpoints
│   ├── services/                          # Risk engine + NLG
│   └── utils/                             # Auth, security utilities
└── ml/                                    # Machine Learning
    ├── requirements.txt                   # ML dependencies
    ├── scripts/                           # Model training scripts
    ├── models/                            # Saved model artifacts
    └── data/                              # Training data (gitignored)
```

---

## 🛠️ Tech Stack

- **Frontend:** HTML5 · CSS3 (Dark Theme + Glassmorphism) · JavaScript ES6+
- **Backend:** Python 3.11+ · FastAPI · SQLAlchemy · Pydantic
- **Databases:** PostgreSQL · Neo4j · Redis
- **ML:** scikit-learn · XGBoost · SHAP · Sentence Transformers
- **Deployment:** Docker Compose · Nginx · GitHub Actions
- **Design Tools:** Figma · Gemini Image Generator

---

## 🚀 Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- [Python 3.11+](https://python.org)
- [Node.js 18+](https://nodejs.org) (optional, for frontend dev server)
- [Docker & Docker Compose](https://docker.com) (for full deployment)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ravindra4158/finsparkk-26.git
   cd finsparkk-26
   ```

2. **Set up the backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate        # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Run the API server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open Swagger UI for the backend:**
   ```text
   http://localhost:8000/api/docs
   ```
   Use the demo credentials `admin` / `admin` in the Swagger Authorize flow.

5. **Open the frontend:**
   ```bash
   # Simply open in your browser:
   open frontend/index.html
   
   # Or use a local server:
   cd frontend && python -m http.server 3000
   ```

6. **View architecture diagrams:**
   ```bash
   open docs/system-architecture-diagrams.html
   ```

---

## 📐 Architecture Diagrams

The project includes **10 detailed, interactive SVG diagrams** in [`docs/system-architecture-diagrams.html`](docs/system-architecture-diagrams.html):

1. System Architecture — Six-module engine overview
2. Entity Relationship Diagram — 10-entity PostgreSQL schema
3. DFD Level 0 — Context diagram
4. DFD Level 1 — Detailed data flows
5. DFD Level 2 — Compliance subsystem detail
6. Sequence Diagram — PNB fraud detection walkthrough
7. Component Architecture — Full stack component view
8. Deployment Architecture — Docker infrastructure
9. Analytics Pipeline — ML processing flow
10. UML Use Case — Actor roles and interactions

---

## 📊 Demo: Catching the PNB Scam in Real-Time

BankGuard detects the ₹485 Cr LoU fraud in **under 60 seconds**:

```
23:47 IST  →  Employee issues LoU MT799 (₹485 Cr)
23:47:02   →  SWIFT/CBS Reconciler: NO CBS RECORD → +45 pts
23:47:05   →  UEBA Engine: 14.2σ from peer baseline → +20 pts
23:47:08   →  Compliance: 48.5× authority limit → +30 pts
23:47:10   →  NLP: Bribery intent 0.91 → +10 pts
23:47:12   →  Graph: 3-hop hidden link → +15 pts
23:47:15   →  Cross-Signal: ALL 5 modules → same person!
23:47:16   →  FINAL SCORE: 100/100 — ⛔ CRITICAL
23:47:17   →  ACTION: FREEZE + REVOKE + SAR + AUDIT NOTE
```

---

## 📋 Full Project Plan

See [**plan.md**](plan.md) for the complete project plan, development phases, module details, and roadmap.

---

## 👥 Team

- **Team Name:** *To be decided*
- **Hackathon:** Finspark '26

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
