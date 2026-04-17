# OTC Process Explorer — Pharma / Life Sciences

Interactive drill-down visualisation of the Order-to-Cash process, showing AI automation opportunities at every level.

## Quick Start

### 1. Backend (Python / FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# API available at http://localhost:8000
```

### 2. Frontend (React / Vite)

```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:5173
```

## How to use

1. The main screen shows the 9 OTC stages as an interactive flow diagram.
2. **Click any stage node** to see its sub-processes in the panel below.
3. **Click any sub-process card** to see individual tasks with AI automation badges.
4. Use the **breadcrumb** at the top to navigate back.

## Automation Types

| Badge | Meaning |
|-------|---------|
| 🤖 Agentic AI | Autonomous multi-step AI agents |
| 🧠 Classical AI / ML | Predictive & analytical ML models |
| 👤 Manual | Human-led process steps |
