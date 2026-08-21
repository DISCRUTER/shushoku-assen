# Shushoku Assen — Backend Test Suite Specification

## Objective
Implement an end-to-end pytest suite for `backend/` per `task.md`. All tests live in `backend/tests/`.
Source code (`backend/application/`, `backend/app.py`, `frontend/`) is **read-only**.

---

## 1. Current Context (Backend Audit)

### Stack
- Flask 3 + flask-smorest (MethodView blueprints, marshmallow validation → 422)
- Flask-SQLAlchemy 3, SQLite (`sqlite:///database.db` in dev — must NOT be touched by tests)
- flask-jwt-extended: JWT in **cookies + headers**, CSRF double-submit enabled for POST/PUT/PATCH/DELETE
- Flask-Caching (SimpleCache), Flask-CORS, Celery (+redis broker), httpx (Google Chat webhooks),
  WeasyPrint (PDF reports), raw smtplib (`application/mail.py`)

### App factory (`app.py`)
- `create_app()` uses `LocalDevelopmentConfig`, registers 9 blueprints:
  `/auth/v1`, `/api/v1/utils`, `/api/v1/students`, `/api/v1/company`, `/api/v1/drives`,
  `/api/v1/applications`, `/api/v1/placements`, `/api/v1/analytics`, `/api/v1/downloads`
- ⚠️ Importing `app.py` executes module-level `data_creation()` → seeds live `database.db`.
  **Tests therefore never import `app.py`; conftest rebuilds the app from `application.factory`
  extensions + blueprint registration with test config.**

### Key behaviors discovered (drive test assertions)
| Area | Behavior |
|---|---|
| Auth | Login sets JWT cookies; blacklisted users → 403; non-approved companies → 403; bad creds → 400; logout requires JWT |
| RBAC | `role_required` (factory.py) reads `role` claim; returns 403 JSON; missing JWT → 401 (flask-jwt-extended); decorator is outermost ⇒ auth checked before schema validation |
| Utils | GET public; POST Admin-only (roles, branch, academic-degree, industry, skills); duplicate name → IntegrityError caught → 500 |
| Students | POST register public (dup email → 409); GET list Admin-only w/ filters (branch_id, year, degree_id, blacklisted, name ilike); GET by id any-authed; PATCH Admin/Student (student only self via identity==email; `blacklisted` key ignored for students); DELETE takes **User id**, Admin/Student |
| Company | POST register public (status defaults PENDING); GET list Admin/Student; PATCH Admin/Company (Company self-only; Company cannot change status/blacklisted — keys popped); DELETE Admin/Company (User id) |
| Drives | GET any-authed w/ filters (company_id LIKE, title ilike, job_type, status); POST Company-only, status forced PENDING, fires `drive_notification.delay(title, company_name)` webhook; PATCH Admin/Company (status enum); DELETE Admin-only → 202 |
| Applications | POST Student-only `{drive_id, student_id}` status forced APPLIED; GET any-authed w/ filters; PATCH Admin/Company (status transitions shortlist/select/reject); no ownership check on student_id (documented behavior) |
| Placements | POST Company-only `{student_id, company_id, drive_id, joining_date}`; GET any-authed; single GET cached 10s |
| Analytics | Any-authed; query flags: students(all/academic_degree/branch-group default), company(all/industry default), drives(all/by_status/by_company/job_type default + company_id HAVING), application(all/by_status + filters), placements(all/default group-by company). Response shape `{"data": [[label, count], ...]}` |
| Downloads | Report triggers return `{"id": task_id}`; role rules per endpoint (admin report=Admin, student=Admin/Student, company/drive=Admin/Company, placement offer=any-authed); poll `GET /downloads/<id>` → 202 pending / 200 file / 500 failed |
| Tasks | `shared_task`s use FlaskTask wrapper (app context pushed on eager run); webhooks via `httpx.post`; PDFs via `HTML(...).write_pdf()` into `static/reports/`; mail via smtplib |

### Enums (`util_enum.py`)
CompanyStatus(pending/approved/rejected), DriveStatus(pending/open/closed/rejected),
ApplicationStatus(applied/shortlisted/selected/rejected/offered), JobType(internship/part-time/full-time)

### Roles seeded by dummy data: `Admin`, `Student`, `Company`

---

## 2. Planning / Architecture Decisions

### Directory layout
```
backend/tests/
├── conftest.py                  # app/client fixtures, auth fixtures, factories import
├── factories.py                 # DB seeding helpers (users, students, companies, drives, ...)
├── unit/
│   ├── test_models.py           # UUID pk, timestamps, relationships, user.details, hashing
│   ├── test_decorators.py       # role_required on minimal Flask+JWT app (200/401/403)
│   └── test_schemas.py          # marshmallow load/dump validation rules
└── integration/
    ├── test_auth.py             # login/logout/CSRF/blacklist/approval gating
    ├── test_utils.py            # CRUD lookups + Admin-only POST (parametrized)
    ├── test_students.py         # register/RBAC/filters/PATCH semantics/delete
    ├── test_company.py          # register/RBAC/approve-reject/self-edit boundaries
    ├── test_drives.py           # create + webhook mock assert, approval workflow, filters
    ├── test_applications.py     # apply/status transitions/cross-user boundaries
    ├── test_placements.py       # offers + viewing rights
    ├── test_analytics.py        # aggregate metrics vs seeded counts
    └── test_downloads.py        # report triggers, eager results, polling, RBAC
```

### Test config (conftest) — isolation guarantees
- `SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"` + `StaticPool` + `check_same_thread=False`
  (single shared in-memory DB across sessions/contexts)
- `CACHE_TYPE = "NullCache"` (Flask-Caching disabled)
- `TESTING = True`; JWT settings copied from dev config; **CSRF kept ON** (realistic flows;
  auth clients auto-send `X-CSRF-TOKEN` from cookie)
- Celery: reuse `celery_init_app(app)` then override → `task_always_eager=True`,
  `task_store_eager_result=True`, `broker_url="memory://"`, `result_backend="cache+memory://"`
  (no redis contact; `AsyncResult` polling works in-process)
- Network/IO mocking strategy:
  - `application.tasks.httpx.post` → MagicMock (webhook dispatch assertions)
  - `application.tasks.HTML.write_pdf` → side-effect writes dummy file into real
    `static/reports/` so download endpoint can serve it; autouse fixture removes created files
  - `application.mail.send_email` / `smtplib.SMTP` → mocked in mail-task tests
- Function-scoped `app` fixture: fresh in-memory DB per test (`create_all` → seed → yield → teardown)

### Auth fixtures
`AuthClient` wrapper adds `X-CSRF-TOKEN` header to mutating verbs.
Fixtures: `unauthenticated_client`, `admin_client`, `student_client`,
`approved_company_client`, `pending_company_client` (pending = logged-in impossible →
fixture provides client + credentials and asserts login is blocked).

### Dependencies added (pyproject.toml `[dependency-groups].dev`)
- `pytest>=8.3` only — pytest-flask unnecessary (hand-rolled fixtures).
- `[tool.pytest.ini_options]`: `testpaths=["tests"]`, `pythonpath=["."]`.

### Run command
```bash
cd backend && uv sync && uv run pytest -q
```

---

## 3. Todo — ALL COMPLETE ✅

- [x] Audit backend source & environment (uv, weasyprint imports OK)
- [x] Add pytest dev-dependency + pytest config to pyproject.toml
- [x] Build backend/tests/conftest.py + factories.py (+ `__init__.py` in tests/, unit/, integration/)
- [x] Unit tests: test_models.py, test_decorators.py, test_schemas.py, test_tasks.py
- [x] Integration: test_auth.py, test_utils.py
- [x] Integration: test_students.py, test_company.py
- [x] Integration: test_drives.py, test_applications.py, test_placements.py
- [x] Integration: test_analytics.py, test_downloads.py
- [x] Run `uv run pytest` inside backend/ → **204 passed, 0 failed (~48s)**

---

## 4. Final Result Summary

### Suite composition (204 tests)
| Module | Coverage |
|---|---|
| unit/test_models.py | UUID pks, timestamps, Werkzeug hashing, `user.details` per role, backrefs, M2M skills, cascade deletes, unique constraints, enum fields |
| unit/test_decorators.py | `role_required`: 401 no-token / 403 wrong-role / 200 match / multi-role lists / missing claim |
| unit/test_schemas.py | Login validation, DriveRegistration rules (title length, openings≥1, enums, dates), update/filter schemas, AnalyticsSchema dump shape |
| unit/test_tasks.py | Webhook post payload + error swallowing, drives_cleanup status flip, mail_student happy path + missing student |
| integration/* | All 9 blueprints: positive, 401/403/422, filters, workflows (approval, blacklist, shortlist→select→reject), CSRF, eager-Celery report triggers + polling |

### Key infrastructure lessons (encoded in conftest)
- Each auth fixture gets its OWN `app.test_client()` — sharing one jar caused cookie overwrites
- `Flask(__name__, root_path=BACKEND_ROOT)` so templates/reports resolve to `backend/`
- `SERVER_NAME="localhost"` required for `url_for` inside tasks outside request context
- Celery eager + `task_store_eager_result=True` + `cache+memory://` backend makes `/downloads/<id>` polling fully in-process

### QA findings — documented (NOT fixed; source is read-only)
1. **Broad `except Exception` swallows `HTTPException`**: abort(404)/abort(403) raised *inside* try-blocks surface as **500** on:
   students GET/PATCH/DELETE unknown-id & cross-user PATCH; company GET/PATCH/DELETE unknown-id & cross-user PATCH; drive GET-single/DELETE unknown-id; application/placement GET-single unknown-id.
   (Endpoints with aborts *outside* try correctly return 404: drive POST unknown company, application PATCH, download triggers.)
2. **Company DELETE has no ownership check**: any approved Company can delete ANY company account (204) — privilege issue.
3. **Application POST ignores caller identity**: any Student can apply as any student_id.
4. **Drive PATCH has no ownership check**: any Company can modify any drive's status.
5. **Company register response dumps `status` as enum NAME (`"PENDING"`)** while filter schemas use values (`"pending"`) — inconsistent API representation.
6. **Utils duplicate names → 500** (IntegrityError swallowed) instead of 409.
7. `User.__repr__` references non-existent `self.username` (would crash on repr) — untested by design.

### Guardrail compliance (verified via git status)
- Only `backend/pyproject.toml` (+uv.lock) modified — dev deps & pytest config
- Zero edits under `backend/application/`, `backend/app.py`, `frontend/`
- No `database.db` created; reports dir auto-cleaned after each test

---

## 5. CI/CD (added post-suite)

`.github/workflows/backend-tests.yml`
- Triggers: push / pull_request → `main`; runner: `ubuntu-latest`; `working-directory: backend`
- Steps: checkout → apt install Pango libs (WeasyPrint import requirement) → `astral-sh/setup-uv@v6`
  (Python 3.13, cached) → `uv sync` (includes dev group) → `uv run pytest -q`
- No Redis service needed: suite uses eager Celery + memory broker/backend
- Concurrency group cancels superseded runs on same ref
