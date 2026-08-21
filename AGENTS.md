# AGENTS.md — Shushoku Assen

Context for AI coding agents working in this repository.

## Project Overview

**Shushoku Assen** is a college placement portal (like "LinkedIn for internal college placements") that streamlines hiring: companies post placement drives, students apply with one click, and admins approve drives/company registrations and manage everything.

Three roles with role-based access control (RBAC) enforced on every endpoint:

- **Admin** — approves drives & company registrations, manages utilities, full access
- **Company** — posts drives, shortlists/selects/rejects applicants, makes placement offers
- **Student** — browses drives, applies, tracks applications/offers

Core resources: **Drive** (job campaign by a company), **Application** (student → drive), **Placement** (offer to a selected student).

## Tech Stack

### Backend (`backend/`) — Python >= 3.13, managed with [uv](https://docs.astral.sh/uv/)

- **Flask 3** + **flask-smorest** — REST API, MethodView blueprints, marshmallow validation (invalid payloads → 422), OpenAPI/Swagger docs at `/swagger-ui`
- **Flask-SQLAlchemy 3** — ORM, SQLite (`sqlite:///database.db`, created + seeded on startup)
- **flask-jwt-extended** — JWT auth stored in **cookies**, CSRF double-submit enabled
- **Flask-Caching** (SimpleCache), **Flask-CORS**
- **Celery + Redis** — async tasks (PDF reports, emails, Google Chat webhooks) and beat schedule (monthly student report mails, daily drive cleanup)
- **WeasyPrint** — PDF report generation into `backend/static/reports/`
- **httpx** — Google Chat webhook calls; raw smtplib for mail (SMTP `localhost:1025`)
- **Werkzeug** — password hashing
- Tests: **pytest**

### Frontend (`frontend/`) — Vue 3 SPA built with Vite

- **Vue 3** + **Vite 7**
- **Pinia** — state management (`src/stores/auth.js`)
- **Vue Router** (`src/router.js`)
- **Chart.js** + vue-chartjs + chartjs-chart-funnel — analytics dashboards
- **Axios** (`src/axios.js` — instance with cookie/CSRF handling), **dayjs**

## Project Structure

```
.
├── backend/
│   ├── app.py                  # Entry point: app factory, blueprint registration,
│   │                           #   celery init + periodic task schedule, DB seeding
│   │                           #   (binds host="0.0.0.0" so port mapping works in Docker)
│   ├── celery_config.py        # Broker/result backend config; reads CELERY_BROKER_URL /
│   │                           #   CELERY_RESULT_BACKEND env vars (default redis://localhost:6379)
│   ├── pyproject.toml          # Deps (uv); pytest config: testpaths=tests, pythonpath=.
│   ├── Dockerfile              # Multi-stage: uv venv build → python:3.13-slim runtime
│   │                           #   (+ Pango/HarfBuzz libs for WeasyPrint, non-root user)
│   ├── .dockerignore           # Excludes .venv, tests/, instance/, generated reports
│   ├── static/reports/         # Generated PDF reports
│   ├── templates/              # HTML templates for WeasyPrint PDFs
│   ├── tests/
│   │   ├── conftest.py         # App/client/auth fixtures (rebuilds app WITHOUT importing app.py)
│   │   ├── factories.py        # DB seeding helpers
│   │   ├── unit/               # Models, decorators, schemas
│   │   └── integration/        # API endpoint tests per resource
│   └── application/
│       ├── api/                # Blueprints: auth.py, utils.py, student.py, company.py,
│       │                       #   drive.py, applied.py, placement.py, analytics.py, download.py
│       ├── factory.py          # Extension singletons (db, api, jwt, cors, cache) +
│       │                       #   role_required decorator
│       ├── models.py           # SQLAlchemy models (UUID string PKs, created_at/updated_at)
│       ├── schema.py           # Marshmallow schemas
│       ├── util_enum.py        # Enums: CompanyStatus, DriveStatus, ApplicationStatus, JobType
│       ├── tasks.py            # Celery tasks (reports, mail, webhook, drive cleanup)
│       ├── celery.py           # celery_init_app (FlaskTask wrapper)
│       ├── mail.py             # SMTP helper
│       ├── config.py           # LocalDevelopmentConfig etc.
│       └── dummy_data.py       # Seeds demo data on startup
├── frontend/
│   ├── vite.config.js          # Proxies /api and /auth → http://127.0.0.1:3000
│   ├── Dockerfile              # Multi-stage: Vite build (node:22) → nginx:alpine
│   ├── nginx.conf              # nginx: SPA fallback; proxies /api, /auth, /swagger-ui,
│   │                           #   /openapi.json → http://backend:3000 (same-origin)
│   ├── .dockerignore           # Excludes node_modules/, dist/
│   └── src/
│       ├── main.js             # App bootstrap (Pinia, router)
│       ├── router.js           # Routes
│       ├── axios.js            # Axios instance (cookies + CSRF)
│       ├── download.js         # Report download/polling helpers
│       ├── stores/auth.js      # Pinia auth store
│       └── components/         # Views grouped by domain: StudentComponent/,
│                               #   CompanyComponent/, DriveComponent/, ApplicationComponent/,
│                               #   ChartComponent/, DashboardPage/, LandingPage/, UtilsComponent/
│                               #   + shared: NavBar.vue, Header.vue, Button.vue, SearchBar.vue, Tooltip.vue
├── specs.md                    # Backend test-suite specification (detailed behavior audit)
├── docker-compose.yml          # Full stack: redis + backend (API) + worker + beat + frontend
└── README.md                   # Full user-facing docs incl. complete API reference
```

## Commands

### Backend

```bash
cd backend
uv sync                          # install deps
uv run python app.py             # API on http://localhost:3000 (seeds SQLite on first run)

# Celery (needs Redis on localhost:6379)
uv run celery -A app.celery worker --loglevel=info
uv run celery -A app.celery beat --loglevel=info

# Tests (never touch the live database.db; conftest builds an isolated app)
uv run pytest
```

### Frontend

```bash
cd frontend
npm install
npm run dev                      # Vite dev server on http://localhost:5173
npm run build                    # production build
```

The Vite dev server proxies `/api` and `/auth` to the backend at `http://127.0.0.1:3000`.

### Docker (full stack)

```bash
docker compose up --build         # API on http://localhost:3000, SPA on http://localhost:5173
docker compose logs -f backend    # follow one service
docker compose down               # stop (named volumes persist)
```

Services: `redis` → `backend` (API) → `worker` + `beat` (same image as backend, command overridden) → `frontend` (nginx).

## Architecture Notes & Conventions

- **App factory**: `create_app()` in `backend/app.py` loads `LocalDevelopmentConfig`, registers 9 blueprints under `/auth/v1` and `/api/v1/{utils,students,company,drives,applications,placements,analytics,downloads}`.
- ⚠️ **Importing `app.py` has side effects**: module-level `data_creation()` seeds the live `database.db`. Tests must NOT import `app.py`; `tests/conftest.py` rebuilds the app from `application.factory` extensions + blueprint registration with a test config instead.
- **Auth flow**: login sets JWT cookies (access token). JWT works via cookies AND headers; CSRF double-submit is required for POST/PUT/PATCH/DELETE from the browser. Frontend's `axios.js` handles this.
- **RBAC**: `role_required` decorator in `application/factory.py` reads the `role` claim; returns 403 JSON when role doesn't match, 401 when JWT missing. The decorator wraps routes outermost ⇒ auth is checked before marshmallow schema validation.
- **Validation**: flask-smorest + marshmallow; invalid request bodies automatically return 422.
- **IDs**: all models use UUID strings as primary keys plus `created_at`/`updated_at`.
- **Enums** (`util_enum.py`): CompanyStatus `pending|approved|rejected`, DriveStatus `pending|open|closed|rejected`, ApplicationStatus `applied|shortlisted|selected|rejected|offered`, JobType `internship|part-time|full-time`.
- **Data model**: `User` (email, hashed password, blacklisted, role FK) with one-one role-dependent detail records (`StudentDetails`, `CompanyDetails`). Utility tables: Role, Branch, AcademicDegree, Industry, Skill (Skill is many-many with both students and drives).
- **Downloads pattern**: report endpoints dispatch a Celery task and return `{"id": task_id}`; clients poll `GET /api/v1/downloads/<id>` → 202 pending / 200 file / 500 failed.
- **Analytics responses** are shaped `{"data": [[label, count], ...]}` for direct Chart.js consumption.
- **CORS**: allowed origins are localhost/127.0.0.1 on ports 3000 and 5173 with credentials.

## Docker Notes

- **Compose topology**: `redis` → `backend` (API, :3000) → `worker` + `beat` (reuse the backend image via `build:` + overridden `command:`) → `frontend` (nginx :5173→80).
- **Volumes**:
  - `sqlite-data → /app/instance` — Flask-SQLAlchemy 3 resolves relative SQLite URIs against the app *instance path*, so the DB lives at `/app/instance/database.db`, NOT `/app/database.db`.
  - `reports → /app/static/reports` — mounted into BOTH `backend` and `worker`: Celery tasks write PDFs here and the API serves them; without the shared mount downloads return nothing.
- **Startup ordering / seeding race**: importing `app.py` runs `data_creation()` (module-level), so api, worker and beat would all try to seed simultaneously. Compose gates worker/beat on `backend: service_healthy`; the healthcheck polls the public `/openapi.json`.
- **Env overrides**: `celery_config.py` reads `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` (defaults `redis://localhost:6379/{0,1}`, so local dev needs no env vars). Compose points them at `redis://redis:6379/{0,1}`.
- **Frontend in Docker is nginx, not Vite dev**: the built SPA is served same-origin with `/api` + `/auth` reverse-proxied to `backend:3000` (`frontend/nginx.conf`), mirroring the Vite dev proxy — JWT cookies + CSRF work without any CORS changes. Frontend code uses relative URLs only.
- Backend image: multi-stage uv sync (`--frozen --no-dev --no-install-project`) into a cached venv layer; WeasyPrint runtime libs installed via apt; runs as non-root user `app`; `instance/` and `static/reports/` are pre-created/chowned so named volumes inherit ownership.

## Demo Accounts (seeded by dummy_data.py)

Password `password` for all:

| Role    | Email               | Notes                        |
| ------- | ------------------- | ---------------------------- |
| Admin   | `user@admin.com`    | Full access                  |
| Student | `user@student1.com` | Branch: Computer Science     |
| Student | `user@student2.com` | Branch: Data Science         |
| Student | `user@student3.com` | Branch: Mechanical Engineering |
| Company | `hr@techcorp.com`   | Approved — can host drives   |
| Company | `hr@financeltd.com` | Pending approval             |
| Company | `hr@badcompany.com` | Rejected                     |

## Where to Look

- Full API endpoint reference (routes, roles, filters): `README.md`
- Detailed backend behavior audit + test plan: `specs.md`
