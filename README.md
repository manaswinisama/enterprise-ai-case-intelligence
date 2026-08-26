# ProcessIQ — Enterprise AI Case Intelligence Platform

ProcessIQ is an enterprise-grade decision-support platform engineered to transform unstructured business workflows into structured, actionable automation and AI adoption strategies. It decomposes operational processes into granular activities, evaluates technical feasibility, maps target technologies (Intelligent Document Processing, RPA, LLMs, Deterministic Rules), flags Human-in-the-Loop (HITL) governance checkpoints, and calculates explainable priority scores for strategic portfolio allocation.

---

## 🏗️ System Architecture

```mermaid
graph TD
    UI[React + Vite Frontend Dashboard] -->|REST API Requests| API[FastAPI Gateway]
    API --> SVC[Process Intelligence Service]
    
    subgraph Core Intelligence Engine
        SVC --> CLS[Activity Classifier & NLP Heuristics]
        CLS --> TECH[Tech Stack Mapping: IDP / RPA / LLM]
        CLS --> HITL[HITL Risk & Compliance Analyzer]
        SVC --> SCORE[Multi-Factor Decision Engine]
    end
    
    subgraph Strategic Portfolio Prioritization
        SCORE -->|Normalized Dimensions| MTRX[2x2 Strategic Matrix: Impact vs Effort]
        MTRX --> QW[Quick Wins]
        MTRX --> SB[Strategic Bets]
        MTRX --> OW[Operational Wins]
        MTRX --> DF[Re-evaluate / Defer]
    end

    SVC --> DB[(SQLite / PostgreSQL ORM)]
    SVC --> REP[Executive Decision Brief]
    REP --> UI```

     Key CapabilitiesActivity-Level Decomposition & Classification: Breaks down end-to-end workflows into discrete tasks and evaluates them across AI Suitability, Automation Feasibility, and Human Oversight needs.Explainable Multi-Factor Prioritization: Replaces black-box scoring with an explainable 5-dimension mathematical model.Strategic 2×2 Portfolio Matrix: Automatically maps organizational processes across four quadrants (Quick Wins, Strategic Bets, Operational Wins, Re-evaluate/Defer).Human-in-the-Loop (HITL) Governance: Detects regulatory, financial, and decision risks requiring mandatory human oversight.Executive Decision Brief: Generates clean, exportable PDF/print summaries for enterprise leadership.📐 Scoring Methodology & Decision MathThe platform evaluates processes across five normalized dimensions ($1.0$ to $5.0$ scale):$I$ (Business Impact): Evaluates volume, cycle time reduction, and operational value.$S$ (AI Suitability): Measures cognitive complexity, unstructured data handling, and NLP/Vision requirements.$F$ (Automation Feasibility): Assesses determinism, rule consistency, and digital data readiness.$E$ (Implementation Effort): Evaluates system touchpoints, integrations, and architectural complexity.$R$ (Governance & Risk): Quantifies regulatory exposure, compliance requirements, and human checkpoint necessity.$$\text{Priority Score} = \min\left(98, \; \max\left(25, \; \left[\frac{I \times S \times F}{E \times R} \times \frac{1}{\kappa}\right] \times 100\right)\right)$$(Where $\kappa = 8.5$ serves as the empirical normalization constant across enterprise benchmark distributions.)🛠️ Technology StackFrontend: React 18, Vite, JavaScript (ES6+), CSS3 Enterprise Design TokensBackend: Python 3.10+, FastAPI, Pydantic v2, UvicornData Layer: SQLite (development) via SQLAlchemy ORM (architected for drop-in PostgreSQL migration)Intelligence Layer: Rule-based heuristic classification and multi-factor analytical scoring pipelines📂 Project Structureenterprise-ai-case-intelligence/
├── backend/
│   ├── main.py                  # FastAPI server entry point and routing
│   ├── scoring_engine.py        # Multi-factor mathematical scoring logic
│   └── seed_data.py             # Database seed script for enterprise workflows
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PrioritizationMatrix.jsx   # 2x2 Portfolio Grid component
│   │   │   ├── ScoreBreakdown.jsx         # 5-Dimension scoring gauge card
│   │   │   └── ExecutiveExportButton.jsx  # One-click report generator
│   │   ├── App.jsx              # Main dashboard application shell
│   │   ├── App.css              # Enterprise design system styles
│   │   └── main.jsx             # Vite mounting point
│   ├── package.json
│   └── vite.config.js
├── processiq.db                 # SQLite local database
├── requirements.txt             # Python dependencies
└── README.md                    # Technical documentation
🚀 Quickstart & Setup Guide1. Backend SetupPowerShell# Navigate to project root
cd enterprise-ai-case-intelligence

# Activate Python virtual environment
.\venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Seed the database with sample operational workflows
python seed_data.py

# Start the FastAPI server
uvicorn main:app --reload --port 8000
API runs at http://127.0.0.1:8000 with interactive Swagger docs at http://127.0.0.1:8000/docs.2. Frontend SetupPowerShell# Open a second terminal and navigate to frontend
cd enterprise-ai-case-intelligence/frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
Dashboard will be available at http://localhost:5173.🔌 API Endpoints1. List All ProcessesEndpoint: GET /processesResponse: Returns array of stored processes with metadata and analysis snapshots.2. Create & Analyze ProcessEndpoint: POST /processesRequest Body:JSON{
  "name": "Invoice Processing",
  "department": "Finance",
  "description": "Extract, validate, and match vendor invoices against POs for payment.",
  "activities": [
    "Receive invoices from vendors",
    "Extract invoice details",
    "Validate invoice information",
    "Match invoice with purchase order",
    "Send invoice for approval",
    "Process payment"
  ]
}
3. Re-evaluate ProcessEndpoint: POST /analyze/{process_id}Response: Full intelligence payload including priority score, 5-dimension metrics, quadrant classification, and activity-level taxonomy.🔒 Enterprise Readiness & GovernanceAuditability: Explainable sub-factor calculations eliminate opaque black-box scoring.Human-in-the-Loop Checks: Automated validation flags ensure high-risk activities retain mandatory human sign-off.Database Agnostic: Built on SQLAlchemy ORM for zero-downtime migration to PostgreSQL in production environments.