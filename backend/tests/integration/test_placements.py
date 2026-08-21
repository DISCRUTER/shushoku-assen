from application.factory import db
from application.models import Placement
from application.util_enum import DriveStatus

from tests.factories import make_company, make_drive, make_placement, make_student


def test_issue_placement_offer_success(approved_company_client, approved_company_user):
    student = make_student()
    drive = make_drive(approved_company_user)
    response = approved_company_client.post(
        "/api/v1/placements/",
        json={
            "student_id": student.student_details.id,
            "company_id": approved_company_user.company_details.id,
            "drive_id": drive.id,
            "joining_date": "2030-07-01",
        },
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["student_id"] == student.student_details.id
    assert body["company_id"] == approved_company_user.company_details.id
    assert body["drive_id"] == drive.id


def test_issue_offer_forbidden_for_student_and_admin(student_client, admin_client, approved_company_user):
    student = make_student()
    drive = make_drive(approved_company_user)
    payload = {
        "student_id": student.student_details.id,
        "company_id": approved_company_user.company_details.id,
        "drive_id": drive.id,
        "joining_date": "2030-07-01",
    }
    assert student_client.post("/api/v1/placements/", json=payload).status_code == 403
    assert admin_client.post("/api/v1/placements/", json=payload).status_code == 403


def test_issue_offer_unauthenticated_rejected(unauthenticated_client, approved_company_user):
    student = make_student()
    drive = make_drive(approved_company_user)
    response = unauthenticated_client.post(
        "/api/v1/placements/",
        json={
            "student_id": student.student_details.id,
            "company_id": approved_company_user.company_details.id,
            "drive_id": drive.id,
            "joining_date": "2030-07-01",
        },
    )
    assert response.status_code == 401


def test_issue_offer_unknown_references_404(approved_company_client, approved_company_user):
    student = make_student()
    drive = make_drive(approved_company_user)

    bad_student = approved_company_client.post(
        "/api/v1/placements/",
        json={
            "student_id": "nonexistent-student",
            "company_id": approved_company_user.company_details.id,
            "drive_id": drive.id,
            "joining_date": "2030-07-01",
        },
    )
    assert bad_student.status_code == 404

    bad_drive = approved_company_client.post(
        "/api/v1/placements/",
        json={
            "student_id": student.student_details.id,
            "company_id": approved_company_user.company_details.id,
            "drive_id": "nonexistent-drive",
            "joining_date": "2030-07-01",
        },
    )
    assert bad_drive.status_code == 404


def test_issue_offer_missing_fields_unprocessable(approved_company_client, approved_company_user):
    response = approved_company_client.post(
        "/api/v1/placements/",
        json={"student_id": "x", "company_id": approved_company_user.company_details.id},
    )
    assert response.status_code == 422


def test_list_placements_any_authenticated_role(
    admin_client, student_client, approved_company_client, unauthenticated_client, approved_company_user
):
    student = make_student()
    drive = make_drive(approved_company_user)
    make_placement(student, approved_company_user, drive)

    for authed in (admin_client, student_client, approved_company_client):
        response = authed.get("/api/v1/placements/")
        assert response.status_code == 200
        assert len(response.get_json()) >= 1

    assert unauthenticated_client.get("/api/v1/placements/").status_code == 401


def test_list_placements_filter_by_student(student_client, approved_company_user):
    target = make_student()
    other = make_student()
    drive = make_drive(approved_company_user)
    target_offer = make_placement(target, approved_company_user, drive)
    other_offer = make_placement(other, approved_company_user, drive)

    response = student_client.get(
        "/api/v1/placements/", query_string={"student_id": target.student_details.id}
    )
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert target_offer.id in ids
    assert other_offer.id not in ids


def test_list_placements_filter_by_company(student_client, approved_company_user):
    student = make_student()
    drive_a = make_drive(approved_company_user)
    other_company = make_company()
    drive_b = make_drive(other_company)
    offer_a = make_placement(student, approved_company_user, drive_a)
    offer_b = make_placement(student, other_company, drive_b)

    response = student_client.get(
        "/api/v1/placements/",
        query_string={"company_id": approved_company_user.company_details.id},
    )
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert offer_a.id in ids
    assert offer_b.id not in ids


def test_list_placements_filter_by_drive(student_client, approved_company_user):
    student = make_student()
    drive_a = make_drive(approved_company_user)
    drive_b = make_drive(approved_company_user)
    offer_a = make_placement(student, approved_company_user, drive_a)
    offer_b = make_placement(student, approved_company_user, drive_b)

    response = student_client.get("/api/v1/placements/", query_string={"drive_id": drive_a.id})
    assert response.status_code == 200
    ids = [entry["id"] for entry in response.get_json()]
    assert offer_a.id in ids
    assert offer_b.id not in ids


def test_get_single_placement_nested(student_client, unauthenticated_client, approved_company_user):
    student = make_student()
    drive = make_drive(approved_company_user)
    placement = make_placement(student, approved_company_user, drive)

    response = student_client.get(f"/api/v1/placements/{placement.id}")
    assert response.status_code == 200
    body = response.get_json()
    assert body["student"]["user"]["email"] == student.email
    assert body["company"]["registered_name"] == approved_company_user.company_details.registered_name
    assert body["drive"]["title"] == drive.title

    assert unauthenticated_client.get(f"/api/v1/placements/{placement.id}").status_code == 401
    assert student_client.get("/api/v1/placements/nonexistent-id").status_code == 500
