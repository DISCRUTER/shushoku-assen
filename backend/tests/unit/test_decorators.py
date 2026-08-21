import pytest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token

from application.factory import role_required


@pytest.fixture()
def mini_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "unit-test-secret"
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    JWTManager(app)

    @app.route("/admin-only")
    @role_required("Admin")
    def admin_only():
        return jsonify(ok=True)

    @app.route("/staff")
    @role_required(["Admin", "Company"])
    def staff_area():
        return jsonify(ok=True)

    return app


def bearer_headers(app, role):
    with app.app_context():
        token = create_access_token(
            identity="user@test.com", additional_claims={"role": role}
        )
    return {"Authorization": f"Bearer {token}"}


def test_missing_token_returns_401(mini_app):
    response = mini_app.test_client().get("/admin-only")
    assert response.status_code == 401


def test_single_role_match_allows_access(mini_app):
    client = mini_app.test_client()
    response = client.get("/admin-only", headers=bearer_headers(mini_app, "Admin"))
    assert response.status_code == 200
    assert response.get_json() == {"ok": True}


def test_single_role_mismatch_forbidden(mini_app):
    client = mini_app.test_client()
    for role in ("Student", "Company"):
        response = client.get("/admin-only", headers=bearer_headers(mini_app, role))
        assert response.status_code == 403
        assert response.get_json()["msg"] == "Access forbidden: Insufficient permissions"


def test_multiple_roles_allow_listed_roles(mini_app):
    client = mini_app.test_client()
    for role in ("Admin", "Company"):
        response = client.get("/staff", headers=bearer_headers(mini_app, role))
        assert response.status_code == 200


def test_multiple_roles_reject_unlisted_role(mini_app):
    response = mini_app.test_client().get("/staff", headers=bearer_headers(mini_app, "Student"))
    assert response.status_code == 403


def test_token_without_role_claim_forbidden(mini_app):
    with mini_app.app_context():
        token = create_access_token(identity="user@test.com")
    response = mini_app.test_client().get(
        "/admin-only", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
