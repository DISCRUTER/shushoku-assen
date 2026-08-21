from application.factory import db
from application.models import Application
from application.util_enum import ApplicationStatus, DriveStatus

from tests.factories import make_application, make_company, make_drive, make_student


def test_apply_to_drive_success(student_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user, status=DriveStatus.OPEN)
    response = student_client.post(
        "/api/v1/applications/",
        json={"drive_id": drive.id, "student_id": student_user.student_details.id},
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["status"] == ApplicationStatus.APPLIED.value
    assert body["drive_id"] == drive.id
    assert body["student_id"] == student_user.student_details.id


def test_apply_forbidden_for_company_and_admin(approved_company_client, admin_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    payload = {"drive_id": drive.id, "student_id": student_user.student_details.id}
    assert approved_company_client.post("/api/v1/applications/", json=payload).status_code == 403
    assert admin_client.post("/api/v1/applications/", json=payload).status_code == 403


def test_apply_unauthenticated_rejected(unauthenticated_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    response = unauthenticated_client.post(
        "/api/v1/applications/",
        json={"drive_id": drive.id, "student_id": student_user.student_details.id},
    )
    assert response.status_code == 401


def test_apply_unknown_drive_404(student_client, student_user):
    response = student_client.post(
        "/api/v1/applications/",
        json={"drive_id": "nonexistent-drive", "student_id": student_user.student_details.id},
    )
    assert response.status_code == 404


def test_apply_unknown_student_404(student_client, approved_company_user):
    drive = make_drive(approved_company_user)
    response = student_client.post(
        "/api/v1/applications/",
        json={"drive_id": drive.id, "student_id": "nonexistent-student"},
    )
    assert response.status_code == 404


def test_apply_missing_student_reference_404(student_client):
    response = student_client.post("/api/v1/applications/", json={"drive_id": "x"})
    assert response.status_code == 404


def test_cross_student_application_not_restricted_documented_behavior(student_client):
    other_student = make_student()
    company = make_company()
    drive = make_drive(company)
    response = student_client.post(
        "/api/v1/applications/",
        json={"drive_id": drive.id, "student_id": other_student.student_details.id},
    )
    assert response.status_code == 201


def test_list_applications_any_authenticated_role(student_client, unauthenticated_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    make_application(student_user, drive)
    ok = student_client.get("/api/v1/applications/")
    assert ok.status_code == 200
    assert len(ok.get_json()) >= 1
    assert unauthenticated_client.get("/api/v1/applications/").status_code == 401


def test_list_applications_filter_by_student(student_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    mine = make_application(student_user, drive)
    someone_else = make_student()
    theirs = make_application(someone_else, drive)

    response = student_client.get(
        "/api/v1/applications/", query_string={"student_id": student_user.student_details.id}
    )
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert mine.id in ids
    assert theirs.id not in ids


def test_list_applications_filter_by_drive(student_client, student_user, approved_company_user):
    target_drive = make_drive(approved_company_user)
    other_drive = make_drive(approved_company_user)
    on_target = make_application(student_user, target_drive)
    on_other = make_application(student_user, other_drive)

    response = student_client.get(
        "/api/v1/applications/", query_string={"drive_id": target_drive.id}
    )
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert on_target.id in ids
    assert on_other.id not in ids


def test_list_applications_filter_by_company(student_client, student_user, approved_company_user):
    other_company = make_company()
    drive_a = make_drive(approved_company_user)
    drive_b = make_drive(other_company)
    app_a = make_application(student_user, drive_a)
    app_b = make_application(student_user, drive_b)

    response = student_client.get(
        "/api/v1/applications/",
        query_string={"company_id": approved_company_user.company_details.id},
    )
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert app_a.id in ids
    assert app_b.id not in ids


def test_get_single_application_nested(student_client, unauthenticated_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive)

    response = student_client.get(f"/api/v1/applications/{application.id}")
    assert response.status_code == 200
    body = response.get_json()
    assert body["drive"]["title"] == drive.title
    assert body["student"]["user"]["email"] == student_user.email

    assert unauthenticated_client.get(f"/api/v1/applications/{application.id}").status_code == 401
    assert student_client.get("/api/v1/applications/nonexistent-id").status_code == 500


def test_patch_shortlist_by_company(approved_company_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive)
    response = approved_company_client.patch(
        f"/api/v1/applications/{application.id}", json={"status": "shortlisted"}
    )
    assert response.status_code == 200
    db.session.expire_all()
    assert db.session.get(Application, application.id).status == ApplicationStatus.SHORTLISTED


def test_patch_accept_by_company(approved_company_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive, status=ApplicationStatus.SHORTLISTED)
    response = approved_company_client.patch(
        f"/api/v1/applications/{application.id}", json={"status": "selected"}
    )
    assert response.status_code == 200
    db.session.expire_all()
    assert db.session.get(Application, application.id).status == ApplicationStatus.SELECTED


def test_patch_reject_by_admin(admin_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive)
    response = admin_client.patch(
        f"/api/v1/applications/{application.id}", json={"status": "rejected"}
    )
    assert response.status_code == 200
    db.session.expire_all()
    assert db.session.get(Application, application.id).status == ApplicationStatus.REJECTED


def test_patch_invalid_status_unprocessable(approved_company_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive)
    response = approved_company_client.patch(
        f"/api/v1/applications/{application.id}", json={"status": "vanished"}
    )
    assert response.status_code == 422


def test_patch_application_forbidden_for_student(student_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive)
    response = student_client.patch(
        f"/api/v1/applications/{application.id}", json={"status": "shortlisted"}
    )
    assert response.status_code == 403


def test_patch_application_unauthenticated_rejected(unauthenticated_client, student_user, approved_company_user):
    drive = make_drive(approved_company_user)
    application = make_application(student_user, drive)
    response = unauthenticated_client.patch(
        f"/api/v1/applications/{application.id}", json={"status": "shortlisted"}
    )
    assert response.status_code == 401


def test_patch_unknown_application_404(approved_company_client):
    response = approved_company_client.patch(
        "/api/v1/applications/nonexistent-id", json={"status": "shortlisted"}
    )
    assert response.status_code == 404
