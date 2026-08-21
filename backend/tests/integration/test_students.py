from application.factory import db
from application.models import User

from tests.factories import (
    DEFAULT_PASSWORD,
    get_or_create_branch,
    get_or_create_degree,
    make_student,
    unique_suffix,
)


def student_payload(**overrides):
    payload = {
        "email": f"new-student-{unique_suffix()}@test.com",
        "password": "super-secret-123",
        "first_name": "New",
        "last_name": "Student",
        "year": 2,
        "cgpa": 8.0,
        "branch_id": get_or_create_branch().id,
        "academic_degree_id": get_or_create_degree().id,
    }
    payload.update(overrides)
    return payload


def test_register_student_success(client):
    payload = student_payload()
    response = client.post("/api/v1/students/", json=payload)
    assert response.status_code == 201
    body = response.get_json()
    assert body["first_name"] == "New"
    assert body["id"]

    login = client.post(
        "/auth/v1/login", json={"email": payload["email"], "password": payload["password"]}
    )
    assert login.status_code == 200
    assert login.get_json()["role"] == "Student"


def test_register_student_duplicate_email_conflict(client, student_user):
    response = client.post(
        "/api/v1/students/", json=student_payload(email=student_user.email)
    )
    assert response.status_code == 409


def test_register_student_missing_required_field_unprocessable(client):
    payload = student_payload()
    del payload["cgpa"]
    response = client.post("/api/v1/students/", json=payload)
    assert response.status_code == 422


def test_register_student_invalid_email_unprocessable(client):
    response = client.post("/api/v1/students/", json=student_payload(email="nope"))
    assert response.status_code == 422


def test_list_students_admin_only(admin_client, student_client, approved_company_client, unauthenticated_client, student_user):
    ok = admin_client.get("/api/v1/students/")
    assert ok.status_code == 200
    emails = [entry["user"]["email"] for entry in ok.get_json()]
    assert student_user.email in emails

    assert student_client.get("/api/v1/students/").status_code == 403
    assert approved_company_client.get("/api/v1/students/").status_code == 403
    assert unauthenticated_client.get("/api/v1/students/").status_code == 401


def test_list_students_filter_by_year(admin_client):
    target = make_student(year=6)
    other = make_student(year=4)
    response = admin_client.get("/api/v1/students/", query_string={"year": 6})
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert target.student_details.id in ids
    assert other.student_details.id not in ids


def test_list_students_filter_by_blacklisted(admin_client):
    flagged = make_student()
    flagged.blacklisted = True
    db.session.commit()
    clean = make_student()

    response = admin_client.get("/api/v1/students/", query_string={"blacklisted": "true"})
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert flagged.student_details.id in ids
    assert clean.student_details.id not in ids


def test_list_students_filter_by_name(admin_client):
    target = make_student(first_name="Zephyrine")
    make_student(first_name="Ordinary")
    response = admin_client.get("/api/v1/students/", query_string={"name": "Zephyrine"})
    assert response.status_code == 200
    entries = response.get_json()
    assert len(entries) == 1
    assert entries[0]["first_name"] == "Zephyrine"


def test_list_students_filter_by_branch(admin_client):
    branch = get_or_create_branch("Mechanical Engineering")
    target = make_student(branch=branch)
    response = admin_client.get(
        "/api/v1/students/", query_string={"branch_id": branch.id}
    )
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert target.student_details.id in ids


def test_get_single_student_any_authenticated_role(student_client, approved_company_client, unauthenticated_client):
    student = make_student()
    student_id = student.student_details.id

    as_student = student_client.get(f"/api/v1/students/{student_id}")
    assert as_student.status_code == 200
    assert as_student.get_json()["user"]["email"] == student.email

    as_company = approved_company_client.get(f"/api/v1/students/{student_id}")
    assert as_company.status_code == 200

    assert unauthenticated_client.get(f"/api/v1/students/{student_id}").status_code == 401
    assert student_client.get("/api/v1/students/nonexistent-id").status_code == 500


def test_patch_admin_can_blacklist_student(admin_client, student_user):
    response = admin_client.patch(
        f"/api/v1/students/{student_user.student_details.id}", json={"blacklisted": True}
    )
    assert response.status_code == 202
    db.session.expire_all()
    assert db.session.get(User, student_user.id).blacklisted is True


def test_patch_admin_blacklist_blocks_login(client, admin_client, student_user):
    admin_client.patch(
        f"/api/v1/students/{student_user.student_details.id}", json={"blacklisted": True}
    )
    login = client.post(
        "/auth/v1/login", json={"email": student_user.email, "password": DEFAULT_PASSWORD}
    )
    assert login.status_code == 403


def test_patch_student_self_profile_edit(student_client, student_user):
    response = student_client.patch(
        f"/api/v1/students/{student_user.student_details.id}",
        json={"about": "Updated about", "github": "https://github.com/new"},
    )
    assert response.status_code == 202
    body = response.get_json()
    assert body["about"] == "Updated about"
    assert body["github"] == "https://github.com/new"


def test_patch_student_cannot_blacklist_self(student_client, student_user):
    response = student_client.patch(
        f"/api/v1/students/{student_user.student_details.id}",
        json={"blacklisted": True, "about": "still editable"},
    )
    assert response.status_code == 202
    db.session.expire_all()
    user = db.session.get(User, student_user.id)
    assert user.blacklisted is False
    assert user.student_details.about == "still editable"


def test_patch_other_student_surfaces_as_server_error_documented_behavior(student_client):
    other = make_student()
    response = student_client.patch(
        f"/api/v1/students/{other.student_details.id}", json={"about": "hijacked"}
    )
    assert response.status_code == 500


def test_patch_student_by_company_forbidden(approved_company_client, student_user):
    response = approved_company_client.patch(
        f"/api/v1/students/{student_user.student_details.id}", json={"about": "nope"}
    )
    assert response.status_code == 403


def test_patch_unknown_student_surfaces_as_server_error_documented_behavior(admin_client):
    response = admin_client.patch("/api/v1/students/nonexistent-id", json={"about": "x"})
    assert response.status_code == 500


def test_delete_student_by_admin(admin_client, client, student_user):
    response = admin_client.delete(f"/api/v1/students/{student_user.id}")
    assert response.status_code == 204
    db.session.expire_all()
    assert db.session.get(User, student_user.id) is None


def test_delete_own_account_by_student(student_client, student_user):
    response = student_client.delete(f"/api/v1/students/{student_user.id}")
    assert response.status_code == 204
    db.session.expire_all()
    assert db.session.get(User, student_user.id) is None


def test_delete_student_by_company_forbidden(approved_company_client, student_user):
    response = approved_company_client.delete(f"/api/v1/students/{student_user.id}")
    assert response.status_code == 403


def test_delete_unknown_student_surfaces_as_server_error_documented_behavior(admin_client):
    response = admin_client.delete("/api/v1/students/nonexistent-id")
    assert response.status_code == 500
