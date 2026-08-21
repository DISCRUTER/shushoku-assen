from unittest.mock import MagicMock

from application import tasks as tasks_module

from tests.factories import make_company, make_drive, make_placement, make_student


def test_admin_report_trigger_admin_only(
    admin_client, student_client, approved_company_client, unauthenticated_client, mock_weasyprint
):
    assert student_client.get("/api/v1/downloads/report").status_code == 403
    assert approved_company_client.get("/api/v1/downloads/report").status_code == 403
    assert unauthenticated_client.get("/api/v1/downloads/report").status_code == 401

    response = admin_client.get("/api/v1/downloads/report")
    assert response.status_code == 200
    assert response.get_json()["id"]


def test_poll_completed_report_serves_file(admin_client, mock_weasyprint):
    task_id = admin_client.get("/api/v1/downloads/report").get_json()["id"]
    response = admin_client.get(f"/api/v1/downloads/{task_id}")
    assert response.status_code == 200
    assert response.data.startswith(b"%PDF-1.4")


def test_poll_failed_report_returns_500(admin_client, monkeypatch):
    def _factory(*args, **kwargs):
        instance = MagicMock()
        instance.write_pdf.side_effect = RuntimeError("pdf engine exploded")
        return instance

    monkeypatch.setattr(tasks_module, "HTML", MagicMock(side_effect=_factory))

    task_id = admin_client.get("/api/v1/downloads/report").get_json()["id"]
    response = admin_client.get(f"/api/v1/downloads/{task_id}")
    assert response.status_code == 500


def test_poll_unknown_task_id_still_generating(admin_client):
    response = admin_client.get("/api/v1/downloads/definitely-not-a-real-task-id")
    assert response.status_code == 202
    assert "generating" in response.get_json()["message"]


def test_student_report_trigger_rbac_and_404(
    admin_client, student_client, approved_company_client, mock_weasyprint
):
    student = make_student()

    as_admin = admin_client.get(f"/api/v1/downloads/student/{student.student_details.id}/report")
    assert as_admin.status_code == 200
    assert as_admin.get_json()["id"]

    as_owner = student_client.get(f"/api/v1/downloads/student/{student.student_details.id}/report")
    assert as_owner.status_code == 200

    assert (
        approved_company_client.get(
            f"/api/v1/downloads/student/{student.student_details.id}/report"
        ).status_code
        == 403
    )
    assert (
        student_client.get("/api/v1/downloads/student/nonexistent-id/report").status_code == 404
    )


def test_company_report_trigger_rbac_and_404(
    admin_client, student_client, approved_company_client, mock_weasyprint
):
    company = make_company()

    as_admin = admin_client.get(f"/api/v1/downloads/company/{company.company_details.id}/report")
    assert as_admin.status_code == 200

    as_self = approved_company_client.get(
        f"/api/v1/downloads/company/{company.company_details.id}/report"
    )
    assert as_self.status_code == 200

    assert (
        student_client.get(f"/api/v1/downloads/company/{company.company_details.id}/report").status_code
        == 403
    )
    assert (
        approved_company_client.get("/api/v1/downloads/company/nonexistent-id/report").status_code
        == 404
    )


def test_drive_report_trigger_rbac_and_404(
    admin_client, student_client, approved_company_client, mock_weasyprint
):
    company = make_company()
    drive = make_drive(company)

    as_admin = admin_client.get(f"/api/v1/downloads/drive/{drive.id}/report")
    assert as_admin.status_code == 200

    as_company = approved_company_client.get(f"/api/v1/downloads/drive/{drive.id}/report")
    assert as_company.status_code == 200

    assert student_client.get(f"/api/v1/downloads/drive/{drive.id}/report").status_code == 403
    assert approved_company_client.get("/api/v1/downloads/drive/nonexistent-id/report").status_code == 404


def test_placement_offer_trigger_any_authenticated_role(
    admin_client, student_client, approved_company_client, unauthenticated_client, mock_weasyprint
):
    company = make_company()
    student = make_student()
    drive = make_drive(company)
    placement = make_placement(student, company, drive)

    for authed in (admin_client, student_client, approved_company_client):
        response = authed.get(f"/api/v1/downloads/placement/{placement.id}/report")
        assert response.status_code == 200
        assert response.get_json()["id"]

    assert (
        unauthenticated_client.get(f"/api/v1/downloads/placement/{placement.id}/report").status_code
        == 401
    )
    assert (
        student_client.get("/api/v1/downloads/placement/nonexistent-id/report").status_code == 404
    )
