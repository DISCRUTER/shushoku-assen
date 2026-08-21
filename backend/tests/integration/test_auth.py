from flask_jwt_extended import create_access_token

from tests.conftest import AuthClient
from tests.factories import DEFAULT_PASSWORD, make_company, make_user


def test_login_success_returns_identity_and_sets_cookies(client, admin_user):
    response = client.post(
        "/auth/v1/login", json={"email": admin_user.email, "password": DEFAULT_PASSWORD}
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["id"] == admin_user.id
    assert body["role"] == "Admin"
    assert client.get_cookie("access_token_cookie") is not None
    assert client.get_cookie("csrf_access_token") is not None


def test_login_wrong_password_rejected(client, admin_user):
    response = client.post(
        "/auth/v1/login", json={"email": admin_user.email, "password": "wrong-password"}
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Invalid credentials."


def test_login_unknown_email_rejected(client):
    response = client.post(
        "/auth/v1/login", json={"email": "ghost@nowhere.com", "password": "whatever"}
    )
    assert response.status_code == 400


def test_login_missing_fields_unprocessable(client):
    response = client.post("/auth/v1/login", json={"email": "user@example.com"})
    assert response.status_code == 422

    response = client.post("/auth/v1/login", json={"password": "secret"})
    assert response.status_code == 422

    response = client.post("/auth/v1/login", json={"email": "not-an-email", "password": "x"})
    assert response.status_code == 422


def test_login_blacklisted_user_forbidden(client):
    blacklisted = make_user(role_name="Student", blacklisted=True)
    response = client.post(
        "/auth/v1/login", json={"email": blacklisted.email, "password": DEFAULT_PASSWORD}
    )
    assert response.status_code == 403
    assert "blacklisted" in response.get_json()["message"]


def test_login_pending_company_forbidden(client, pending_company_user):
    response = client.post(
        "/auth/v1/login", json={"email": pending_company_user.email, "password": DEFAULT_PASSWORD}
    )
    assert response.status_code == 403
    assert "not approved" in response.get_json()["message"]


def test_login_rejected_company_forbidden(client):
    from application.util_enum import CompanyStatus

    rejected_company = make_company(status=CompanyStatus.REJECTED)
    response = client.post(
        "/auth/v1/login",
        json={"email": rejected_company.email, "password": DEFAULT_PASSWORD},
    )
    assert response.status_code == 403


def test_login_approved_company_succeeds(client, approved_company_user):
    response = client.post(
        "/auth/v1/login", json={"email": approved_company_user.email, "password": DEFAULT_PASSWORD}
    )
    assert response.status_code == 200
    assert response.get_json()["role"] == "Company"


def test_logout_requires_authentication(client):
    response = client.post("/auth/v1/logout")
    assert response.status_code == 401


def test_logout_clears_cookies(app, admin_user):
    raw = app.test_client()
    login = raw.post(
        "/auth/v1/login", json={"email": admin_user.email, "password": DEFAULT_PASSWORD}
    )
    assert login.status_code == 200
    assert raw.get_cookie("access_token_cookie") is not None

    csrf = raw.get_cookie("csrf_access_token").value
    authed = AuthClient(raw, csrf)
    response = authed.post("/auth/v1/logout")
    assert response.status_code == 200
    assert response.get_json()["msg"] == "Access Token removed!"
    assert raw.get_cookie("access_token_cookie") is None


def test_mutation_without_csrf_token_rejected(client, admin_user):
    login_response = client.post(
        "/auth/v1/login", json={"email": admin_user.email, "password": DEFAULT_PASSWORD}
    )
    assert login_response.status_code == 200

    no_csrf_response = client.post("/api/v1/utils/roles", json={"name": "No Csrf Role"})
    assert no_csrf_response.status_code == 401


def test_header_bearer_token_bypasses_csrf(app, client):
    with app.app_context():
        token = create_access_token(
            identity="admin@header.test", additional_claims={"role": "Admin"}
        )
    response = client.post(
        "/api/v1/utils/roles",
        json={"name": "Header Role"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_full_cookie_flow_end_to_end(client, admin_user):
    login = client.post(
        "/auth/v1/login", json={"email": admin_user.email, "password": DEFAULT_PASSWORD}
    )
    assert login.status_code == 200
    csrf = client.get_cookie("csrf_access_token").value
    authed = AuthClient(client, csrf)

    created = authed.post("/api/v1/utils/roles", json={"name": "Flow Role"})
    assert created.status_code == 201

    listed = authed.get("/api/v1/utils/roles")
    names = [role["name"] for role in listed.get_json()]
    assert "Flow Role" in names
