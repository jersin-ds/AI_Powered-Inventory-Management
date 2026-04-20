# AI Powered Inventory Management System — Setup & Run Guide

## Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **pnpm** (`npm install -g pnpm`)

---

## 1. Backend Setup (FastAPI)

Open a terminal and run these commands **in order**:

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment (first time only)
python -m venv venv

# Activate the virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Seed the database with sample data (creates inventory.db)
python -m inventory_backend.seed

# Start the backend server (runs on http://localhost:8000)
python -m uvicorn inventory_backend.app.main:app --reload --port 8000
```

> **API Docs:** Once running, visit http://localhost:8000/docs for Swagger UI.

---

## 2. Frontend Setup (React + Vite)

Open a **second terminal** and run:

```bash
# Navigate to the frontend folder
cd frontend

# Install dependencies (first time only)
pnpm install

# Start the development server (runs on http://localhost:5173)
pnpm dev
```

> **App URL:** Open http://localhost:5173 in your browser.

---

## 3. Demo Login Credentials

| Role              | Email                    | Password      |
|-------------------|--------------------------|---------------|
| Admin             | admin@inventory.com      | password123   |
| Inventory Manager | manager@inventory.com    | password123   |
| Sales Staff       | sales@inventory.com      | password123   |

---

## 4. Quick Reference — All Commands

| Task                        | Command                                                              |
|-----------------------------|----------------------------------------------------------------------|
| Activate venv (PowerShell)  | `cd backend ; .\venv\Scripts\Activate.ps1`                           |
| Install backend deps        | `pip install -r requirements.txt`                                    |
| Seed database               | `python -m inventory_backend.seed`                                   |
| Start backend               | `python -m uvicorn inventory_backend.app.main:app --reload --port 8000` |
| Install frontend deps       | `cd frontend ; pnpm install`                                        |
| Start frontend              | `cd frontend ; pnpm dev`                                            |
| Build frontend for prod     | `cd frontend ; pnpm build`                                          |
| Re-seed (reset data)        | Delete `backend/inventory.db` then run the seed command again        |

---

## 5. Project Structure

```
├── backend/                  # FastAPI backend
│   ├── inventory_backend/
│   │   ├── app/
│   │   │   ├── main.py       # FastAPI app entry point
│   │   │   ├── routes/       # API route handlers
│   │   │   ├── services/     # Business logic
│   │   │   ├── repositories/ # Database queries
│   │   │   ├── models/       # SQLAlchemy models
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   ├── auth/         # JWT authentication
│   │   │   └── ai/           # AI service (Cerebras)
│   │   └── seed.py           # Database seeder
│   ├── requirements.txt
│   └── .env                  # Environment variables
│
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   └── app/
│   │       ├── pages/        # All page components
│   │       ├── components/   # Reusable UI components
│   │       ├── services/     # API client (axios)
│   │       └── store/        # Zustand state management
│   └── package.json
│
└── start-project.md          # This file
```

---

## 6. Troubleshooting

- **Backend won't start?** Make sure the virtual environment is activated (`venv`) before running uvicorn.
- **Frontend API errors?** Ensure the backend is running on port 8000 first.
- **Login not working?** Run the seed command to populate the database with demo users.
- **Want fresh data?** Delete `backend/inventory.db` and re-run `python -m inventory_backend.seed`.
