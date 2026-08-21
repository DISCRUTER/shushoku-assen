from application.factory import db
from application.models import Drive
from application.util_enum import CompanyStatus, DriveStatus, JobType

from tests.factories import make_company, make_drive, unique_suffix


def drive_payload(company_user, **overrides):
    payload = {
        "title": f"Graduate SDE Role {unique_suffix()}",
        "description": "Build great software with us.",
        "openings": 5,
        "salary": 800000,
        "job_type": JobType.FULL_TIME.value,
        "deadline": "2030-06-30",
        "company_id": company_user.company_details.id,
    }
    payload.update(overrides)
    return payload


def test_create_drive_as_approved_company(approved_company_client, approved_company_user, mock_httpx_post):
    payload = drive_payload(approved_company_user)
    response = approved_company_client.post("/api/v1/drives/", json=payload)
    assert response.status_code == 201
    body = response.get_json()
    assert body["status"] == DriveStatus.PENDING.value
    assert body["title"] == payload["title"]

    db.session.expire_all()
    stored = db.session.get(Drive, body["id"])
    assert stored is not None
    assert stored.status == DriveStatus.PENDING

    mock_httpx_post.assert_called_once()
    _, kwargs = mock_httpx_post.call_args
    assert payload["title"] in kwargs["json"]["text"]
    assert approved_company_user.company_details.registered_name in kwargs["json"]["text"]


def test_create_drive_forbidden_for_student_and_admin(student_client, admin_client, approved_company_user):
    assert (
        student_client.post("/api/v1/drives/", json=drive_payload(approved_company_user)).status_code
        == 403
    )
    assert (
        admin_client.post("/api/v1/drives/", json=drive_payload(approved_company_user)).status_code
        == 403
    )


def test_create_drive_unauthenticated_rejected(unauthenticated_client, approved_company_user):
    response = unauthenticated_client.post("/api/v1/drives/", json=drive_payload(approved_company_user))
    assert response.status_code == 401


def test_create_drive_unknown_company_404(approved_company_client):
    payload = {
        "title": f"Orphan Drive {unique_suffix()}",
        "description": "No company behind this.",
        "openings": 5,
        "salary": 100000,
        "job_type": JobType.FULL_TIME.value,
        "deadline": "2030-06-30",
        "company_id": "nonexistent-company-id",
    }
    response = approved_company_client.post("/api/v1/drives/", json=payload)
    assert response.status_code == 404


def test_create_drive_title_too_short_unprocessable(approved_company_client, approved_company_user):
    response = approved_company_client.post(
        "/api/v1/drives/", json=drive_payload(approved_company_user, title="abc")
    )
    assert response.status_code == 422


def test_create_drive_zero_openings_unprocessable(approved_company_client, approved_company_user):
    response = approved_company_client.post(
        "/api/v1/drives/", json=drive_payload(approved_company_user, openings=0)
    )
    assert response.status_code == 422


def test_list_drives_any_authenticated_role(student_client, unauthenticated_client, approved_company_user):
    make_drive(approved_company_user)
    ok = student_client.get("/api/v1/drives/")
    assert ok.status_code == 200
    assert len(ok.get_json()) >= 1
    assert unauthenticated_client.get("/api/v1/drives/").status_code == 401


def test_list_drives_filter_by_job_type(student_client, approved_company_user):
    internship = make_drive(approved_company_user, job_type=JobType.INTERNSHIP)
    full_time = make_drive(approved_company_user, job_type=JobType.FULL_TIME)

    response = student_client.get("/api/v1/drives/", query_string={"job_type": "internship"})
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert internship.id in ids
    assert full_time.id not in ids


def test_list_drives_filter_by_status(student_client, approved_company_user):
    open_drive = make_drive(approved_company_user, status=DriveStatus.OPEN)
    pending_drive = make_drive(approved_company_user, status=DriveStatus.PENDING)

    response = student_client.get("/api/v1/drives/", query_string={"status": "open"})
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert open_drive.id in ids
    assert pending_drive.id not in ids


def test_list_drives_filter_by_title(student_client, approved_company_user):
    target = make_drive(approved_company_user, title="Nebula Platform Engineer")
    make_drive(approved_company_user, title="Ordinary Role")
    response = student_client.get("/api/v1/drives/", query_string={"title": "Nebula"})
    assert response.status_code == 200
    entries = response.get_json()
    assert len(entries) == 1
    assert entries[0]["id"] == target.id


def test_get_single_drive_nested_company(student_client, approved_company_user, unauthenticated_client):
    drive = make_drive(approved_company_user, skills=["Python"])
    response = student_client.get(f"/api/v1/drives/{drive.id}")
    assert response.status_code == 200
    body = response.get_json()
    assert body["company"]["registered_name"] == approved_company_user.company_details.registered_name
    assert body["company"]["user"]["email"] == approved_company_user.email

    assert unauthenticated_client.get(f"/api/v1/drives/{drive.id}").status_code == 401
    assert student_client.get("/api/v1/drives/nonexistent-id").status_code == 500


def test_patch_admin_approval_workflow(admin_client, approved_company_user):
    drive = make_drive(approved_company_user, status=DriveStatus.PENDING)

    approve = admin_client.patch(f"/api/v1/drives/{drive.id}", json={"status": "open"})
    assert approve.status_code == 200
    db.session.expire_all()
    assert db.session.get(Drive, drive.id).status == DriveStatus.OPEN

    close = admin_client.patch(f"/api/v1/drives/{drive.id}", json={"status": "closed"})
    assert close.status_code == 200
    db.session.expire_all()
    assert db.session.get(Drive, drive.id).status == DriveStatus.CLOSED


def test_patch_invalid_status_unprocessable(admin_client, approved_company_user):
    drive = make_drive(approved_company_user)
    response = admin_client.patch(f"/api/v1/drives/{drive.id}", json={"status": "exploded"})
    assert response.status_code == 422


def test_patch_own_drive_by_company_allowed(approved_company_client, approved_company_user):
    drive = make_drive(approved_company_user, status=DriveStatus.PENDING)
    response = approved_company_client.patch(f"/api/v1/drives/{drive.id}", json={"status": "open"})
    assert response.status_code == 200
    db.session.expire_all()
    assert db.session.get(Drive, drive.id).status == DriveStatus.OPEN


def test_patch_other_company_drive_not_restricted_documented_behavior(approved_company_client):
    other = make_company()
    drive = make_drive(other, status=DriveStatus.PENDING)
    response = approved_company_client.patch(f"/api/v1/drives/{drive.id}", json={"status": "open"})
    assert response.status_code == 200


def test_patch_unknown_drive_404(admin_client):
    response = admin_client.patch("/api/v1/drives/nonexistent-id", json={"status": "open"})
    assert response.status_code == 404


def test_delete_drive_admin_only(
    admin_client, approved_company_client, student_client, unauthenticated_client, approved_company_user
):
    drive = make_drive(approved_company_user)
    assert student_client.delete(f"/api/v1/drives/{drive.id}").status_code == 403
    assert approved_company_client.delete(f"/api/v1/drives/{drive.id}").status_code == 403
    assert unauthenticated_client.delete(f"/api/v1/drives/{drive.id}").status_code == 401

    response = admin_client.delete(f"/api/v1/drives/{drive.id}")
    assert response.status_code == 202
    db.session.expire_all()
    assert db.session.get(Drive, drive.id) is None


def test_delete_unknown_drive_surfaces_as_server_error_documented_behavior(admin_client):
    response = admin_client.delete("/api/v1/drives/nonexistent-id")
    assert response.status_code == 500
