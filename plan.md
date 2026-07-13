# BankGuard Enterprise — Project Plan 🛡️

> **Hackathon:** Finspark '26  
> **Project:** BankGuard Enterprise — Behavioral Threat & Fraud Detection for Banking  
> **Last Updated:** 2026-07-13

---

## 📌 Problem Statement

Indian banks lose **₹100+ Crores annually** to internal fraud, insider threats, and compliance gaps. The **PNB-Nirav Modi scam (₹11,400 Cr)** exposed critical failures where LoUs were issued without security, records weren't maintained in CBS, and shell companies received massive loans.

Fraud in banking occurs across four major vectors:
1. **By Customers:** Cheque kiting, wrongful chargebacks, loan fraud (fake documents), money laundering.
2. **By Managers & Employees (Our Main Focus):** Embezzlement, account manipulation ("ghost" accounts), data theft, bribery, privilege misuse, and unauthorized fund transfers.
3. **By Contractors & Vendors:** Billing schemes, cyber infiltration, skimming devices.
4. **Social Engineering:** Phishing, "Boss" scams.

Because insiders (bosses, tellers, loan officers) have direct access to core systems, banks cannot rely on basic security. **BankGuard Enterprise** is an AI-powered, multi-module system that tracks smart technology, strict rules, and psychological monitoring to catch these insider threats in real-time.

---

## 🏗️ System Architecture

> **📐 Full Architecture Diagrams:** [system-architecture-diagrams.html](docs/system-architecture-diagrams.html)
>
> The architecture document contains **10 detailed SVG diagrams**:
> 1. System Architecture — Six-module analytics engine overview
> 2. Entity Relationship Diagram — PostgreSQL schema with 10 core entities
> 3. DFD Level 0 (Context) — System boundary and external entities
> 4. DFD Level 1 (Data Flow) — Detailed data flow between all 6 processes
> 5. DFD Level 2 (Compliance) — SWIFT/CBS reconciliation decomposition
> 6. Sequence Diagram — PNB/Nirav Modi fraud detection scenario
> 7. Component Architecture — React + FastAPI + ML service layers
> 8. Deployment Architecture — Docker containerized infrastructure
> 9. Analytics Pipeline — End-to-end ML processing flow
> 10. UML Use Case Diagram — Actor roles and system interactions

---

## 🧩 Project Structure

```
finsparkk-26/
├── README.md                              # Project overview & quick start
├── plan.md                                # This file — full project plan
├── hackathon fraud to bank.txt            # Original requirements & concepts
├── docs/
│   ├── system-architecture-diagrams.html  # 10 interactive SVG architecture diagrams
│   └── bankguard-architecture.svg         # Standalone system architecture SVG
├── frontend/
│   ├── index.html                         # Full single-page dashboard app
│   ├── css/
│   │   └── styles.css                     # Complete dark-theme design system
│   ├── js/
│   │   └── app.js                         # SPA routing, rendering, & charts
│   └── assets/                            # Images, icons, fonts
├── backend/
│   ├── main.py                            # FastAPI app entry point
│   ├── config.py                          # Environment configuration
│   ├── requirements.txt                   # Python dependencies
│   ├── models/
│   │   ├── database.py                    # SQLAlchemy ORM models (10 entities)
│   │   └── schemas.py                     # Pydantic request/response schemas
│   ├── routes/
│   │   ├── auth.py                        # JWT authentication & RBAC
│   │   ├── alerts.py                      # Alert CRUD & statistics
│   │   ├── loans.py                       # Loan management & risk analysis
│   │   └── swift.py                       # SWIFT/CBS reconciliation
│   ├── services/
│   │   ├── risk_engine.py                 # 5-module risk scoring + meta engine
│   │   └── nlg_engine.py                  # Natural language explanation generator
│   └── utils/
│       └── security.py                    # JWT tokens, password hashing, RBAC
└── ml/
    ├── requirements.txt                   # ML-specific dependencies
    ├── models/                            # Trained model artifacts (.pkl, .joblib)
    ├── scripts/
    │   ├── train_ueba.py                  # Isolation Forest UEBA training
    │   └── train_loan_model.py            # XGBoost loan fraud model training
    └── data/                              # Training datasets (not committed)
```

---

## 🔧 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, Vanilla JS | High-performance SPA with premium UI |
| **Backend** | Python 3.11+, FastAPI | REST API + WebSocket server |
| **Database** | PostgreSQL | Primary relational data store |
| **Graph DB** | Neo4j | Relationship/collusion graph analysis |
| **Cache** | Redis | Alert caching, WebSocket pub/sub |
| **ML - UEBA** | scikit-learn (Isolation Forest) | Employee behavioral anomaly detection |
| **ML - Loan** | XGBoost + SHAP | Explainable loan fraud probability |
| **ML - NLP** | Sentence Transformers | Communication intent classification |
| **ML - Graph** | Neo4j + Louvain algorithm | Collusion cluster detection |
| **ML - Compliance** | JSON Policy Engine | SWIFT/CBS reconciliation rules |
| **Explanation** | NLG Engine (template-based) | Auditor-readable risk explanations |
| **Deployment** | Docker Compose | Containerized multi-service deployment |
| **CI/CD** | GitHub Actions | Automated testing & deployment |

---

## 🧠 Six Analytics Modules

### Module 1: UEBA (User & Entity Behavior Analytics)
- **Objective:** Track manager/employee profiles and catch abnormal activity.
- **Metrics Tracked:** Login/logout time, location, IP address, device, behavioral biometrics (typing speed), files accessed, number of loans approved, average approval amounts.
- **Detection Example (Rajesh the Manager):** Normally logs in at 9:15 AM, approves 5 loans/day (Avg ₹15L), views 20 files. Today, he logged in at 2:30 AM from home, approved 18 loans (Avg ₹3.5 Cr), and viewed 450 files. → **High Risk Score**.

### Module 2: Intelligent Loan Approval Monitoring
- **Objective:** Detect insider fraud during the loan approval process.
- **Metrics Tracked:** Missing verifications, unusually fast approvals, high-value anomalies, same applicant recurring, same property reused, same manager repeatedly approving risky loans.
- **Algorithm:** XGBoost classifier + SHAP explainability.

### Module 3: Compliance & Policy Validation Engine
- **Objective:** Ensure all loans and transactions follow strict bank checkpoints.
- **Checkpoints:** KYC, Income, Property, Credit Score, Background Check, Senior Approval.
- **Detection Example:** If an employee skips the "Income Verification" step for a large loan. → **Alert generated & Loan held**.

### Module 4: Communication Intelligence (NLP)
- **Objective:** Detect suspicious intent, code words, and attempts to evade official channels.
- **Inputs:** Emails, Teams chats, internal logs.
- **Detection Example:** Shifting from "Please upload your KYC" to "Let's discuss on WhatsApp" or using code words like *Gift*, *Package*, *Special Client*, *VIP*, *Fast Track*.

### Module 5: Relationship & Network Analysis (Graph Analytics)
- **Objective:** Map out hidden relationships to find collusion and conflict of interest.
- **Connected Entities:** Manager, Brother, Property, Applicant, Vendor, Bank Account, IP, Phone.
- **Detection Example:** `Applicant` → `Property ID 101` → `Manager's Brother` → `Same Address`. → **Critical Alert**.

### Module 6: AI Risk Scoring & Decision Engine
- **Objective:** Combine all 5 module scores to make a final meta-decision.
- **Action Workflow:** Combines UEBA (e.g., 20) + Loan Behavior (30) + Compliance (25) + NLP (10) + Graph (15) = 100 Total.
- **Recommended Actions:** Monitor, Notify, Hold Loan, Freeze Account, Escalate to Audit Team.

---

## 🚀 Development Phases

### Phase 1: Foundation (Day 1) ✅
- [x] Project setup & repository initialization
- [x] Architecture design & 10 SVG diagrams
- [x] Directory structure (frontend / backend / ml / docs)
- [x] Integrate full problem context (insider threats, specific examples) into `plan.md`

### Phase 2: Frontend Dashboard (Day 1-2) ✅
- [x] Premium dark-theme dashboard with glassmorphism
- [x] Single Page Application (SPA) routing
- [x] Real-time alert panel with risk badges
- [x] Loan review queue, SWIFT/CBS monitor, Graph interface, and Reports views
- [x] Fully functional UI with mock data for the hackathon presentation

### Phase 3: Backend Core (Day 2)
- [ ] FastAPI app setup with CORS, error handling
- [ ] SQLAlchemy models for all 10 database entities
- [ ] Pydantic schemas for request/response validation
- [ ] JWT authentication & role-based access control
- [ ] Alert CRUD endpoints with pagination & filtering

### Phase 4: ML Pipeline (Day 2-3)
- [ ] UEBA Isolation Forest model training script
- [ ] XGBoost loan fraud model with SHAP integration
- [ ] Risk engine service (5 module scores → meta score)
- [ ] NLP and Graph dummy integrations for the demo scenario

### Phase 5: Integration & Demo (Day 3)
- [ ] Connect frontend SPA to FastAPI backend
- [ ] WebSocket integration for live alerts
- [ ] End-to-end PNB fraud scenario demo
- [ ] Final testing, polish, and presentation prep

---

## 🎯 Key Differentiators

1. **Cross-Signal Correlation** — Unlike single-module systems, BankGuard correlates signals across ALL 5 modules. A medium-risk SWIFT gap + medium UEBA anomaly + medium authority breach all pointing at the same person triggers a CRITICAL alert.
2. **PNB-Proof Design** — The SWIFT/CBS reconciler is specifically designed to catch the exact gap that enabled the ₹11,400 Cr PNB scam.
3. **Psychological & Behavioral Monitoring** — Tracks insider actions down to login times and out-of-band communication attempts ("Let's discuss on WhatsApp").
4. **Explainable AI** — Every risk score comes with SHAP-based attribution and NLG-generated natural language explanations, grounded strictly in model output for regulatory compliance.

---

## 📊 Demo Scenario: PNB/Nirav Modi Detection

The demo walks through how BankGuard would have caught the PNB scam in real-time:

1. **23:47 IST** — Employee issues ₹485 Cr LoU via SWIFT MT799
2. **SWIFT/CBS Reconciler** detects: NO CBS record for this LoU → +45 risk points
3. **UEBA Engine** flags: Login at 23:47 is 14.2σ from peer baseline → +20 points
4. **Compliance Engine** flags: Amount is 48.5× officer's authority limit → +30 points
5. **NLP Analyzer** flags: Bribery intent score 0.91 in recent comms → +10 points
6. **Graph Engine** flags: 3-hop hidden link to beneficiary → +15 points
7. **Cross-Signal Correlator**: ALL 5 modules flag SAME person → correlation bonus
8. **Meta Risk Engine**: Final Score = **100/100 — CRITICAL**
9. **Action**: Account FROZEN, credentials REVOKED, SAR queued, audit trail generated
10. **NLG Engine**: Human-readable explanation generated for auditor

> See the full sequence diagram in [system-architecture-diagrams.html](docs/system-architecture-diagrams.html) (Tab 6).

---

## 📝 License

This project is open-source and available under the **MIT License**.
