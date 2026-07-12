# EcoSphere — Architecture

## Backend: Layered Architecture

```
HTTP Request
    ↓
API Router  (app/api/)         — validates input, calls service
    ↓
Service     (app/services/)    — business logic, orchestrates repositories
    ↓
Repository  (app/repositories/)— DB queries via SQLAlchemy (no raw SQL)
    ↓
PostgreSQL
```

**Rule:** Never put business logic or raw SQL in route handlers.

## AI: Isolated Module

```
app/ai/gemini_client.py   — Gemini wrapper with try/except fallback
app/ai/esg_summary.py     — pulls from repositories, prompts Gemini
app/ai/carbon_insights.py
app/ai/audit_summary.py
app/ai/policy_explainer.py
app/api/ai.py             — exposes /api/ai/* endpoints
```

If `GEMINI_API_KEY` is missing or the API is down, every function returns a safe fallback string. The rest of the app never sees an exception from AI.

## Frontend: Module Architecture

```
app/layout.tsx             — root: mounts NatureBackground + CustomCursor + ToastProvider
app/(auth)/login/          — unauthenticated pages
app/(app)/layout.tsx       — auth guard + Sidebar
app/(app)/dashboard/       — Divija's page
app/(app)/environmental/   — Poojitha's page
app/(app)/social/          — Divija's page
app/(app)/governance/      — Pavan's page
app/(app)/gamification/    — Pavan's page
app/(app)/reports/         — Divija's page
app/(app)/ai-insights/     — Poojitha's page
app/(app)/settings/        — Mohan's page
```

State management: Zustand (`authStore`) — token + user persisted to localStorage.
API calls: axios instance in `app/services/api.ts` auto-attaches Bearer token.

## ESG Score Calculation

```
Department Total Score =
  (environmental_score × env_weight + social_score × social_weight + governance_score × gov_weight)
  ÷ (env_weight + social_weight + gov_weight)

Org ESG Score = average of all Department Total Scores

Weights are configurable in Settings (default 40/30/30, must sum to 100).
```
