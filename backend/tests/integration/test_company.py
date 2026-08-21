from application.factory import db
from application.util_enum import CompanyStatus

from tests.factories import (
    DEFAULT_PASSWORD,
    get_or_create_industry,
    make_company,
    unique_suffix,
)


def company_payload(**overrides):
    suffix = unique_suffix()
    payload = {
        "email": f"new-company-{suffix}@test.com",
        "password": "super-secret-123",
        "registered_name": f"Brand New Corp {suffix}",
        "description": "We do things.",
        "location": "Testville",
        "contact_email": f"hello-{suffix}@brandnew.test",
        "contact_phone": str(8000000000 + (int(suffix, 16) % 999999999)),
        "website": f"https://www.brandnew{suffix}.com",
        "industry_id": get_or_create_industry().id,
    }
    payload.update(overrides)
    return payload


def test_register_company_success_defaults_pending(client):
    payload = company_payload()
    response = client.post("/api/v1/company/", json=payload)
    assert response.status_code == 201
    body = response.get_json()
    assert body["registered_name"] == payload["registered_name"]
    assert body["status"] == CompanyStatus.PENDING.name


def test_register_company_duplicate_email_conflict(client, approved_company_user):
    response = client.post(
        "/api/v1/company/", json=company_payload(email=approved_company_user.email)
    )
    assert response.status_code == 409


def test_register_company_missing_required_field_unprocessable(client):
    payload = company_payload()
    del payload["website"]
    response = client.post("/api/v1/company/", json=payload)
    assert response.status_code == 422


def test_list_companies_admin_and_student_only(
    admin_client, student_client, approved_company_client, unauthenticated_client
):
    assert admin_client.get("/api/v1/company/").status_code == 200
    assert student_client.get("/api/v1/company/").status_code == 200
    assert approved_company_client.get("/api/v1/company/").status_code == 403
    assert unauthenticated_client.get("/api/v1/company/").status_code == 401


def test_list_companies_filter_by_status(admin_client):
    pending = make_company(status=CompanyStatus.PENDING)
    approved = make_company(status=CompanyStatus.APPROVED)

    response = admin_client.get("/api/v1/company/", query_string={"status": "pending"})
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert pending.company_details.id in ids
    assert approved.company_details.id not in ids


def test_list_companies_filter_by_name(admin_client):
    target = make_company(registered_name="Quixotic Quantum Systems")
    make_company(registered_name="Mundane Solutions")
    response = admin_client.get("/api/v1/company/", query_string={"name": "Quixotic"})
    assert response.status_code == 200
    entries = response.get_json()
    assert len(entries) == 1
    assert entries[0]["registered_name"] == "Quixotic Quantum Systems"


def test_get_single_company_any_authenticated_role(student_client, admin_client, unauthenticated_client):
    company = make_company()
    company_id = company.company_details.id

    as_admin = admin_client.get(f"/api/v1/company/{company_id}")
    assert as_admin.status_code == 200
    assert as_admin.get_json()["user"]["email"] == company.email

    assert student_client.get(f"/api/v1/company/{company_id}").status_code == 200
    assert unauthenticated_client.get(f"/api/v1/company/{company_id}").status_code == 401
    assert admin_client.get("/api/v1/company/nonexistent-id").status_code == 500


def test_patch_admin_approves_pending_company(client, admin_client, pending_company_user):
    response = admin_client.patch(
        f"/api/v1/company/{pending_company_user.company_details.id}",
        json={"status": "approved"},
    )
    assert response.status_code == 202
    db.session.expire_all()
    assert pending_company_user.company_details.status == CompanyStatus.APPROVED

    login = client.post(
        "/auth/v1/login",
        json={"email": pending_company_user.email, "password": DEFAULT_PASSWORD},
    )
    assert login.status_code == 200


def test_patch_admin_rejects_company(admin_client, pending_company_user):
    response = admin_client.patch(
        f"/api/v1/company/{pending_company_user.company_details.id}",
        json={"status": "rejected"},
    )
    assert response.status_code == 202
    db.session.expire_all()
    assert pending_company_user.company_details.status == CompanyStatus.REJECTED


def test_patch_admin_blacklists_company(admin_client, approved_company_user):
    response = admin_client.patch(
        f"/api/v1/company/{approved_company_user.company_details.id}",
        json={"blacklisted": True},
    )
    assert response.status_code == 202
    db.session.expire_all()
    assert approved_company_user.blacklisted is True


def test_patch_company_self_edit(approved_company_client, approved_company_user):
    response = approved_company_client.patch(
        f"/api/v1/company/{approved_company_user.company_details.id}",
        json={"description": "Fresh description", "location": "New City"},
    )
    assert response.status_code == 202
    db.session.expire_all()
    details = approved_company_user.company_details
    assert details.description == "Fresh description"
    assert details.location == "New City"


def test_patch_company_cannot_change_own_status(approved_company_client, approved_company_user):
    response = approved_company_client.patch(
        f"/api/v1/company/{approved_company_user.company_details.id}",
        json={"status": "rejected"},
    )
    assert response.status_code == 202
    db.session.expire_all()
    assert approved_company_user.company_details.status == CompanyStatus.APPROVED


def test_patch_other_company_surfaces_as_server_error_documented_behavior(approved_company_client):
    other = make_company()
    response = approved_company_client.patch(
        f"/api/v1/company/{other.company_details.id}", json={"description": "hijacked"}
    )
    assert response.status_code == 500


def test_patch_unknown_company_surfaces_as_server_error_documented_behavior(admin_client):
    response = admin_client.patch("/api/v1/company/nonexistent-id", json={"description": "x"})
    assert response.status_code == 500


def test_delete_company_by_admin(admin_client, pending_company_user):
    response = admin_client.delete(f"/api/v1/company/{pending_company_user.id}")
    assert response.status_code == 204
    db.session.expire_all()
    from application.models import User

    assert db.session.get(User, pending_company_user.id) is None


def test_delete_own_company_account(approved_company_client, approved_company_user):
    response = approved_company_client.delete(f"/api/v1/company/{approved_company_user.id}")
    assert response.status_code == 204
    db.session.expire_all()
    from application.models import User

    assert db.session.get(User, approved_company_user.id) is None


def test_delete_other_company_not_restricted_documented_behavior(approved_company_client):
    other = make_company()
    response = approved_company_client.delete(f"/api/v1/company/{other.id}")
    assert response.status_code == 204
    db.session.expire_all()
    from application.models import User

    assert db.session.get(User, other.id) is None


def test_delete_unknown_company_surfaces_as_server_error_documented_behavior(admin_client):
    response = admin_client.delete("/api/v1/company/nonexistent-id")
    assert response.status_code == 500
