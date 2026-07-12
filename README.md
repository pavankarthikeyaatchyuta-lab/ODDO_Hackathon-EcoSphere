# EcoSphere — ESG Management Platform

An ERP module for measuring, managing, and improving an organization's
Environmental, Social, and Governance (ESG) performance — built for the
Odoo Hiring Hackathon 2026.

EcoSphere integrates operational data, employee participation, and
compliance activity into one unified dashboard, and uses gamification to
drive sustainable behavior across the organization.

## Team — PhoenixCore

| Member | Role |
|---|---|
| Pavan | Team Lead — Governance & Gamification, Deployment |
| Mohan | Backend Lead — Architecture, Auth, ESG Scoring, Business Rules |
| Poojitha | Environmental Module + AI Assistant |
| Divija | Social Module + Dashboard/Reports UI |

## Core Modules

- **Environmental** — Emission Factors, Carbon Transactions, Sustainability
  Goals, Environmental Reports
- **Social** — CSR Activities, Employee Participation, Diversity Metrics,
  Training
- **Governance** — ESG Policies, Policy Acknowledgements, Audits,
  Compliance Issues
- **Gamification** — Challenges, XP, Badges, Rewards, Redemption,
  Leaderboard
- **Dashboard** — Organization ESG Score, Department Scores, KPIs, Charts,
  Notifications
- **Reports** — Environmental / Social / Governance / Summary reports with
  filters, exportable as CSV, PDF, and Excel
- **AI Assistant** — Executive ESG summaries, carbon insights, audit
  summaries, and plain-English policy explanations (Gemini)
- **Settings & Administration** — Departments, Categories, Notification
  Settings, and configurable business-rule toggles

## Business Rules

EcoSphere enforces the following as core logic, not just CRUD:

1. **Reward Redemption** — employees redeem earned XP for rewards, subject
   to stock availability; XP and stock are deducted atomically.
2. **Notification System** — in-app/email alerts for new compliance
   issues, CSR/Challenge approval decisions, policy reminders, and badge
   unlocks.
3. **Auto Emission Calculation** — when enabled, Carbon Transactions are
   generated automatically from linked Purchase/Manufacturing/Expense/
   Fleet records using the relevant Emission Factor.
4. **Evidence Requirement** — when enabled, CSR participation cannot be
   approved without an attached proof file.
5. **Badge Auto-Award** — badges are assigned automatically once an
   employee's XP or completed-challenge count satisfies the badge's
   unlock rule.
6. **Compliance Ownership** — every Compliance Issue requires an assigned
   Owner and Due Date; overdue open issues are flagged automatically.

The organization's overall ESG Score is a weighted average of department
scores — default **Environmental 40% / Social 30% / Governance 30%**,
configurable per organization in Settings.

## Tech Stack

**Frontend:** Next.js, React, TypeScript, Tailwind CSS, Zustand, Recharts

**Backend:** FastAPI (Python), layered architecture —
`API → Services → Repositories → PostgreSQL`

**Database:** PostgreSQL, SQLAlchemy ORM

**AI:** Gemini, isolated in `backend/app/ai/` so AI availability never
affects core functionality

**Infra:** Docker / docker-compose for local development

## Project Structure

```
EcoSphere/
├── docker-compose.yml
├── .env.example
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   └── SETUP.md
├── backend/
│   └── app/
│       ├── core/          # config, DB session, auth/security
│       ├── models/        # SQLAlchemy models
│       ├── schemas/       # Pydantic request/response schemas
│       ├── repositories/  # database access layer
│       ├── services/      # business logic
│       ├── api/           # FastAPI routers
│       ├── ai/            # Gemini integration
│       └── tests/
└── frontend/
    └── app/
        ├── components/
        ├── hooks/
        ├── stores/         # Zustand
        ├── types/
        ├── services/       # API clients
        └── lib/
```

## Getting Started

> Setup is being finalized as the project comes together — this section
> will be filled in with exact commands once `docker-compose.yml` and
> `.env.example` are in place. Current expected flow:

```bash
git clone <repo-url>
cd EcoSphere
cp .env.example .env   # fill in DB credentials + GEMINI_API_KEY
docker compose up --build
```

- Backend API docs (Swagger): `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

Full instructions will live in `docs/SETUP.md`.

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — backend architecture
  and design decisions
- [`docs/DATABASE_SCHEMA.md`](docs/DATABASE_SCHEMA.md) — full database
  schema and entity relationships
- [`docs/SETUP.md`](docs/SETUP.md) — detailed local setup guide

## License

TBD.
