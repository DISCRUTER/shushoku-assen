# Shushoku Assen

A placement portal that streamlines the hiring process, helping companies find the best talent and students the best opportunities.

> [!NOTE]
> This project is kind of like `Linkedin - Social Networking` for internal placements in college.

## Highlights

- **Role based access** for Admin, Company and Student (`role_required` on endpoints)
- Browse live placement drives and **apply to a drive with a single click**
- Track every application and placement offer in one place
- Companies can **post drives, shortlist candidates, and manage the entire recruitment pipeline**
- Admin approves drives and company registrations
- **Visualization dashboards** built with Chart.js
- **Filter-driven analytics** (students, companies, drives, applications and placements)
- **On-demand PDF reports** for admin, student, company, drive and placement offer
- **Periodic report emails** dispatched to students with their placement activity attached
- **Google Chat notification** when a new drive opens
- **Secure password hashing** (werkzeug) and **JWT cookie-based session handling**
- Background scheduling with **Celery + Redis** (report mails and drive cleanup)

## Tech Stack

### Backend (`backend/`)
- [Flask](https://flask.palletsprojects.com/) + [Flask-Smorest](https://flask-smorest.readthedocs.io/) — REST API with OpenAPI/Swagger docs (`/swagger-ui`)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) — JWT auth with cookie + CSRF support
- [Flask-Caching](https://flask-caching.readthedocs.io/) — response caching
- [Flask-CORS](https://flask-cors.readthedocs.io/) — cross-origin support
- [Celery](https://docs.celeryq.dev/) + Redis — async tasks, webhooks and scheduled jobs
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/) — PDF report generation
- [httpx](https://www.python-httpx.org/) — Google Chat webhook calls
- [Werkzeug](https://werkzeug.palletsprojects.com/) — password hashing

### Frontend (`frontend/`)
- [Vue 3](https://vuejs.org/) + [Vite](https://vite.dev/)
- [Pinia](https://pinia.vuejs.org/) — state management
- [Vue Router](https://router.vuejs.org/) — routing
- [Chart.js](https://www.chartjs.org/) + [vue-chartjs](https://vue-chartjs.org/) — dashboards (incl. funnel chart)
- [Axios](https://axios-http.com/) — HTTP client
- [dayjs](https://day.js.org/) — date handling

## Project Structure

```
.
├── backend/                       # Flask API + Celery tasks
│   ├── app.py                     # App factory, blueprints, celery schedule
│   ├── celery_config.py           # Broker / result backend config
│   ├── pyproject.toml             # Python deps (uv)
│   └── application/
│       ├── api/                   # Blueprints: auth, utils, student, company,
│       │                          #   drive, applied, placement, analytics, download
│       ├── models.py              # SQLAlchemy models
│       ├── schema.py              # Marshmallow schemas
│       ├── tasks.py               # Celery tasks (reports, mail, webhooks, cleanup)
│       ├── mail.py                # SMTP mail helper
│       ├── dummy_data.py          # Seeds DB with demo data on startup
│       └── factory.py             # Extension init + role_required decorator
└── frontend/                      # Vue 3 + Vite SPA
    ├── index.html
    └── src/
        ├── router.js              # Vue Router routes
        ├── stores/auth.js         # Pinia auth store
        ├── axios.js               # Axios instance with CSRF/cookie handling
        └── components/            # Views & reusable components
```

## Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) with Docker Compose (full-stack deployment), **or** for local development:
  - Python **>= 3.13** ([uv](https://docs.astral.sh/uv/) recommended)
  - Node.js + npm
  - [Redis](https://redis.io/) (Celery broker, default `localhost:6379`)

### Docker (full stack)

One command builds and starts every service — Redis, the Flask API, Celery worker + beat, and the frontend (production build served by nginx):

```bash
docker compose up --build
```

| Service   | URL                                  |
| --------- | ------------------------------------ |
| Frontend  | http://localhost:5173                |
| API       | http://localhost:3000                |
| Swagger   | http://localhost:3000/swagger-ui     |

How it works:

- Services start in order: `redis` → `backend` (API) → `worker` + `beat` (reuse the backend image with overridden commands) → `frontend`.
- `worker` and `beat` wait on the API healthcheck (`GET /openapi.json`) so the SQLite database is seeded exactly once.
- Data persists across restarts in named volumes:
  - `sqlite-data` → `/app/instance/database.db` (SQLite database)
  - `reports` → `/app/static/reports` (generated PDFs, written by the worker and served by the API)
- Celery connects to Redis via `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` (`redis://redis:6379/{0,1}`).
- The frontend container serves the built SPA same-origin and reverse-proxies `/api` and `/auth` to the backend, so JWT cookies + CSRF work without CORS changes.

Useful commands:

```bash
docker compose logs -f backend    # follow one service
docker compose down               # stop (named volumes persist)
docker compose down -v            # stop and wipe the database + reports
```

### Backend (local development)

```bash
cd backend
uv sync                  # install dependencies
uv run python app.py     # start the API on http://localhost:3000
```

- On startup the app creates the SQLite database (`database.db`) and **seeds it with demo data**.
- Interactive API docs are available at `http://localhost:3000/swagger-ui`.

#### Celery (worker + beat)

```bash
# terminal 1 - worker
uv run celery -A app.celery worker --loglevel=info

# terminal 2 - beat (scheduled tasks)
uv run celery -A app.celery beat --loglevel=info
```

Scheduled tasks (defined in `app.py`):
- **Monthly** — emails each student their placement activity report.
- **Daily** — closes drives whose deadline has passed.

#### Mail sink

Report emails use SMTP on `localhost:1025` (see `application/mail.py`). Point a local mail catcher like [MailHog](https://github.com/mailhog/MailHog) or `aiosmtpd` at that port to inspect outgoing mail.

#### Google Chat webhook

The `drive_notification` task posts to a Google Chat webhook when a drive is created. Set the webhook URL in `backend/application/tasks.py`.

### Frontend

```bash
cd frontend
npm install
npm run dev      # start the Vite dev server on http://localhost:5173
```

The Vite dev server proxies `/api` and `/auth` to the backend at `http://127.0.0.1:3000` (see `frontend/vite.config.js`).

### Demo Accounts

Seeded by `backend/application/dummy_data.py`, password `password` for all:

| Role    | Email                    | Notes                                  |
| ------- | ------------------------ | -------------------------------------- |
| Admin   | `user@admin.com`         | Full access                            |
| Student | `user@student1.com`      | Branch: Computer Science               |
| Student | `user@student2.com`      | Branch: Data Science                   |
| Student | `user@student3.com`      | Branch: Mechanical Engineering         |
| Company | `hr@techcorp.com`        | Approved — can host drives             |
| Company | `hr@financeltd.com`      | Pending approval                       |
| Company | `hr@badcompany.com`      | Rejected                               |

## Entities

- **Student** — applies to drives.
- **Company** — hosts drives.
- **Admin** — approves drives and company registrations, manages utilities.

## Resources

- **Drive** — campaign started by a company, approved by Admin, participated in by students.
- **Application** — submitted by a student for a drive.
- **Placement** — offer made to a selected student.

## API Endpoints

All endpoints except `POST /auth/v1/login`, `POST /auth/v1/logout`, `POST /api/v1/students/` and `POST /api/v1/company/` require authentication (JWT). `*` indicates any authenticated user.

### Auth — prefix `/auth/v1`

- **POST** `/auth/v1/login` — Log in with email + password. -> All
- **POST** `/auth/v1/logout` — Log out and clear the access cookie. -> All

### Utilities — prefix `/api/v1/utils`

- **GET** `/api/v1/utils/roles` : Get all roles. -> All
- **POST** `/api/v1/utils/roles` : Create a role. -> Admin
- **GET** `/api/v1/utils/branch` : Get all branches. -> All
- **POST** `/api/v1/utils/branch` : Create a branch. -> Admin
- **GET** `/api/v1/utils/academic-degree` : Get all academic degrees. -> All
- **POST** `/api/v1/utils/academic-degree` : Create an academic degree. -> Admin
- **GET** `/api/v1/utils/industry` : Get all industries. -> All
- **POST** `/api/v1/utils/industry` : Create an industry. -> Admin
- **GET** `/api/v1/utils/skills` : Get all skills. -> All
- **POST** `/api/v1/utils/skills` : Create a skill. -> Admin

### Students — prefix `/api/v1/students`

- **GET** `/api/v1/students/` : Get all students (filter by branch, year, degree, name, blacklisted). -> Admin
- **POST** `/api/v1/students/` : Register a student. -> All (open)
- **GET** `/api/v1/students/<student_id>` : Retrieve a student's profile. -> All authenticated
- **PATCH** `/api/v1/students/<student_id>` : Update the profile (only Admin may set `blacklisted`). -> Student & Admin
- **DELETE** `/api/v1/students/<student_id>` : Delete a student. -> Student & Admin

### Companies — prefix `/api/v1/company`

- **GET** `/api/v1/company/` : Get all companies (filter by industry, status, name, blacklisted). -> Admin & Student
- **POST** `/api/v1/company/` : Register a company. -> All (open)
- **GET** `/api/v1/company/<company_id>` : Retrieve a company's profile. -> All authenticated
- **PATCH** `/api/v1/company/<company_id>` : Update company info (only Admin may set `status`/`blacklisted`). -> Admin & Company
- **DELETE** `/api/v1/company/<company_id>` : Delete a company. -> Admin & Company

### Drives — prefix `/api/v1/drives`

- **GET** `/api/v1/drives/` : Get all drives (filter by company, title, job_type, status). -> All authenticated
- **POST** `/api/v1/drives/` : Create a drive (triggers Google Chat notification). -> Company
- **GET** `/api/v1/drives/<drive_id>` : Retrieve drive info. -> All authenticated
- **PATCH** `/api/v1/drives/<drive_id>` : Update drive info (e.g. approve, change status). -> Admin & Company
- **DELETE** `/api/v1/drives/<drive_id>` : Delete a drive. -> Admin

### Applications — prefix `/api/v1/applications`

- **GET** `/api/v1/applications/` : Get applications (filter by student, drive, company). -> All authenticated
- **POST** `/api/v1/applications/` : Apply to a drive. -> Student
- **GET** `/api/v1/applications/<application_id>` : Retrieve an application. -> All authenticated
- **PATCH** `/api/v1/applications/<application_id>` : Update application status (shortlist / select / reject / offer). -> Admin & Company

### Placements — prefix `/api/v1/placements`

- **GET** `/api/v1/placements/` : Get placement offers (filter by student, company, drive). -> All authenticated
- **POST** `/api/v1/placements/` : Offer a placement. -> Company
- **GET** `/api/v1/placements/<placement_id>` : Retrieve a placement offer. -> All authenticated

### Analytics — prefix `/api/v1/analytics`

- **GET** `/api/v1/analytics/students` : Students by branch / academic degree / total. -> All authenticated
- **GET** `/api/v1/analytics/company` : Companies by industry / total. -> All authenticated
- **GET** `/api/v1/analytics/drives` : Drives by status / job type / top companies / total. -> All authenticated
- **GET** `/api/v1/analytics/application` : Applications by status / total (filter by student, drive, company). -> All authenticated
- **GET** `/api/v1/analytics/placements` : Placements by company / total (filter by student, company, drive). -> All authenticated

### Downloads — prefix `/api/v1/downloads`

Report endpoints dispatch a Celery task and return a task `id`; fetch the finished file from `GET /api/v1/downloads/<id>`.

- **GET** `/api/v1/downloads/report` : Generate the admin report (PDF). -> Admin
- **GET** `/api/v1/downloads/student/<student_id>/report` : Generate a student report (PDF). -> Admin & Student
- **GET** `/api/v1/downloads/company/<company_id>/report` : Generate a company report (PDF). -> Admin & Company
- **GET** `/api/v1/downloads/drive/<drive_id>/report` : Generate a drive report (PDF). -> Admin & Company
- **GET** `/api/v1/downloads/placement/<placement_id>/report` : Generate a placement offer (PDF). -> All authenticated
- **GET** `/api/v1/downloads/<id>` : Retrieve a generated report by task id. -> All authenticated

## Models and Fields

### Base Model (abstract)

- `id` — UUID string (primary key)
- `created_at` — timestamp
- `updated_at` — timestamp

### Utility Models

- **Role** : Base Model
    - `name`, `description`
    - `users` — one-many, users with this role

- **Branch** : Base Model
    - `name`, `description`
    - `students` — one-many, students in this branch

- **AcademicDegree** : Base Model
    - `name`, `description`
    - `students` — one-many, students of this degree

- **Industry** : Base Model
    - `name`, `description`
    - `companies` — one-many, companies in this industry

- **Skill** : Base Model
    - `name`, `description`
    - linked to students (`student_skills`) and drives (`skills_required`) via many-many join tables

### User Models

- **User** : Base Model
    - `email` — unique
    - `password` — hashed (werkzeug)
    - `blacklisted` — boolean
    - `role_id` — FK to `roles.id`
    - `student_details` / `company_details` — one-one, role dependent
    - `details` — property resolving the role-appropriate details object

- **Details (abstract)**
    - `id` — FK to `users.id`

- **StudentDetails** : Details
    - `first_name`, `last_name`
    - `about`
    - `github`, `linkedin`
    - `branch_id` — FK to `branches.id`
    - `year`
    - `academic_degree_id` — FK to `academic_degrees.id`
    - `cgpa`
    - `skills` — many-many with `skills`
    - `applications` — one-many with `applications`
    - `placements` — one-many with `placements`

- **CompanyDetails** : Details
    - `registered_name`
    - `description`
    - `industry_id` — FK to `industries.id`
    - `location`
    - `contact_email`
    - `contact_phone`
    - `website`
    - `status` — enum: `pending` | `approved` | `rejected`
    - `drives` — one-many with `drives`
    - `placements` — one-many with `placements`

### Operational Models

- **Drive** : Base Model
    - `company_id` — FK to `company_details.id`
    - `title`, `description`
    - `openings`
    - `salary`
    - `job_type` — enum: `internship` | `part-time` | `full-time`
    - `deadline`
    - `status` — enum: `pending` | `open` | `closed` | `rejected`
    - `skills_required` — many-many with `skills`
    - `applications` — one-many with `applications`
    - `placements` — one-many with `placements`

- **Application** : Base Model
    - `drive_id` — FK to `drives.id`
    - `student_id` — FK to `student_details.id`
    - `status` — enum: `applied` | `shortlisted` | `selected` | `rejected` | `offered`

- **Placement** : Base Model
    - `student_id` — FK to `student_details.id`
    - `company_id` — FK to `company_details.id`
    - `drive_id` — FK to `drives.id`
    - `joining_date`