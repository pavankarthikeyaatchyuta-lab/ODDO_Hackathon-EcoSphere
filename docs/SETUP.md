# EcoSphere — Setup Guide

## Prerequisites
- Docker & Docker Compose
- Git
- A Gemini API key (get one at aistudio.google.com)

## Quick Start

```bash
git clone <repo-url>
cd EcoSphere
cp .env.example .env
# Edit .env: set GEMINI_API_KEY and change SECRET_KEY
docker compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## First-time seed

After startup, register an admin user:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@eco.com","full_name":"Admin","password":"admin1234","role":"admin"}'
```

Then login at http://localhost:3000/login.

## Local development (without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env   # set DATABASE_URL to local postgres
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| DATABASE_URL | yes | PostgreSQL connection string |
| SECRET_KEY | yes | JWT signing key (change in prod) |
| GEMINI_API_KEY | yes | Google Gemini API key |
| NEXT_PUBLIC_API_URL | yes | Backend base URL for frontend |
