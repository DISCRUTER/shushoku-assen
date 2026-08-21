import os
from datetime import timedelta
from unittest.mock import MagicMock

import httpx
import pytest
from flask import Flask
from sqlalchemy.pool import StaticPool

from application.celery import celery_init_app
from application.factory import api, cache, cors, db, jwt
from application.util_enum import CompanyStatus

from tests.factories import (
    DEFAULT_PASSWORD,
    ensure_base_lookups,
    make_company,
    make_student,
    make_user,
)


BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestConfig:
    TESTING = True
    API_TITLE = "Placement Portal"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    SERVER_NAME = "localhost"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False},
    }
    JWT_SECRET_KEY = "test-secret-key-never-used-in-production"
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_COOKIE_SECURE = False
    JWT_SESSION_COOKIE = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    JWT_COOKIE_CSRF_PROTECT = True
    CACHE_TYPE = "NullCache"


def create_test_app():
    app = Flask(__name__, root_path=BACKEND_ROOT)
    app.config.from_object(TestConfig)

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    api.init_app(app)

    from application.api.analytics import analytics
    from application.api.applied import applications
    from application.api.auth import auth
    from application.api.company import company
    from application.api.download import downloads
    from application.api.drive import drives
    from application.api.placement import placements
    from application.api.student import students
    from application.api.utils import utils

    for blueprint in (
        auth,
        utils,
        students,
        company,
        drives,
        applications,
        placements,
        analytics,
        downloads,
    ):
        api.register_blueprint(blueprint)

    cors.init_app(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

    celery_app = celery_init_app(app)
    celery_app.conf.update(
        broker_url="memory://",
        result_backend="cache+memory://",
        task_always_eager=True,
        task_store_eager_result=True,
    )
    celery_app.set_default()
    return app


class AuthClient:
    def __init__(self, client, csrf_token=None):
        self.client = client
        self.csrf_token = csrf_token

    def _headers(self, extra=None):
        headers = dict(extra or {})
        if self.csrf_token:
            headers.setdefault("X-CSRF-TOKEN", self.csrf_token)
        return headers

    def open(self, url, method="GET", json=None, **kwargs):
        headers = self._headers(kwargs.pop("headers", None))
        return self.client.open(url, method=method, json=json, headers=headers, **kwargs)

    def get(self, url, **kwargs):
        return self.open(url, method="GET", **kwargs)

    def post(self, url, json=None, **kwargs):
        return self.open(url, method="POST", json=json, **kwargs)

    def put(self, url, json=None, **kwargs):
        return self.open(url, method="PUT", json=json, **kwargs)

    def patch(self, url, json=None, **kwargs):
        return self.open(url, method="PATCH", json=json, **kwargs)

    def delete(self, url, **kwargs):
        return self.open(url, method="DELETE", **kwargs)


def perform_login(client, email, password=DEFAULT_PASSWORD):
    response = client.post("/auth/v1/login", json={"email": email, "password": password})
    assert response.status_code == 200, f"Login failed for {email}: {response.get_json()}"
    csrf_cookie = client.get_cookie("csrf_access_token")
    return AuthClient(client, csrf_cookie.value if csrf_cookie else None)


@pytest.fixture()
def app():
    app = create_test_app()
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    ensure_base_lookups()
    yield app
    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def unauthenticated_client(app):
    return AuthClient(app.test_client())


@pytest.fixture()
def admin_user(app):
    return make_user(role_name="Admin")


@pytest.fixture()
def admin_client(app, admin_user):
    return perform_login(app.test_client(), admin_user.email)


@pytest.fixture()
def student_user(app):
    return make_student()


@pytest.fixture()
def student_client(app, student_user):
    return perform_login(app.test_client(), student_user.email)


@pytest.fixture()
def approved_company_user(app):
    return make_company(status=CompanyStatus.APPROVED)


@pytest.fixture()
def approved_company_client(app, approved_company_user):
    return perform_login(app.test_client(), approved_company_user.email)


@pytest.fixture()
def pending_company_user(app):
    return make_company(status=CompanyStatus.PENDING)


@pytest.fixture()
def pending_company_client(app, client, pending_company_user):
    response = client.post(
        "/auth/v1/login",
        json={"email": pending_company_user.email, "password": DEFAULT_PASSWORD},
    )
    assert response.status_code == 403
    return AuthClient(client)


@pytest.fixture(autouse=True)
def mock_httpx_post(monkeypatch):
    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json.return_value = {"ok": True}
    mock = MagicMock(return_value=response_mock)
    monkeypatch.setattr(httpx, "post", mock)
    return mock


@pytest.fixture(autouse=True)
def clean_reports_dir(app):
    reports_dir = os.path.join(app.root_path, "static", "reports")
    existing = set(os.listdir(reports_dir)) if os.path.isdir(reports_dir) else set()
    yield
    if os.path.isdir(reports_dir):
        for name in os.listdir(reports_dir):
            if name not in existing:
                os.remove(os.path.join(reports_dir, name))


@pytest.fixture()
def mock_weasyprint(monkeypatch, app):
    from application import tasks as tasks_module

    def _write_pdf(target=None, **kwargs):
        os.makedirs(os.path.dirname(str(target)), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(b"%PDF-1.4 fake-report-bytes")
        return None

    def _factory(*args, **kwargs):
        instance = MagicMock()
        instance.write_pdf.side_effect = _write_pdf
        return instance

    html_factory = MagicMock(side_effect=_factory)
    monkeypatch.setattr(tasks_module, "HTML", html_factory)
    return html_factory


@pytest.fixture()
def mock_send_email(monkeypatch):
    from application import tasks as tasks_module

    mock = MagicMock(return_value=True)
    monkeypatch.setattr(tasks_module, "send_email", mock)
    return mock
