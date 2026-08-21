from datetime import date, timedelta

from application.tasks import drive_notification, drives_cleanup, mail_student
from application.util_enum import DriveStatus

from tests.factories import make_company, make_drive, make_student


def test_drive_notification_posts_webhook(app, mock_httpx_post):
    result = drive_notification("SDE Intern", "Tech Corp")
    assert result == "The message is sent."
    mock_httpx_post.assert_called_once()
    args, kwargs = mock_httpx_post.call_args
    assert "SDE Intern" in kwargs["json"]["text"]
    assert "Tech Corp" in kwargs["json"]["text"]


def test_drive_notification_swallows_request_errors(app, monkeypatch):
    import httpx

    def boom(*args, **kwargs):
        raise httpx.ConnectError("no network")

    monkeypatch.setattr(httpx, "post", boom)
    result = drive_notification("Title", "Company")
    assert result == "The message is sent."


def test_drives_cleanup_closes_expired_open_drives(app):
    company = make_company()
    expired = make_drive(company, status=DriveStatus.OPEN, deadline=date.today() - timedelta(days=1))
    active = make_drive(company, status=DriveStatus.OPEN, deadline=date.today() + timedelta(days=10))
    closed = make_drive(company, status=DriveStatus.CLOSED)

    result = drives_cleanup()

    assert result == "Drive cleanup completed."
    assert db_status_of(expired) == DriveStatus.CLOSED
    assert db_status_of(active) == DriveStatus.OPEN
    assert db_status_of(closed) == DriveStatus.CLOSED


def db_status_of(drive):
    from application.factory import db
    from application.models import Drive

    db.session.expire_all()
    return db.session.get(Drive, drive.id).status


def test_mail_student_sends_report_email(app, mock_weasyprint, mock_send_email):
    student = make_student(email="mailme@test.com")
    result = mail_student.delay(student.student_details.id).result
    assert "Report emailed successfully to mailme@test.com" in result
    mock_send_email.assert_called_once()
    _, kwargs = mock_send_email.call_args
    assert kwargs["to_address"] == "mailme@test.com"
    assert kwargs["attachment_file"].endswith(".pdf")


def test_mail_student_reports_missing_student(app, mock_weasyprint, mock_send_email):
    result = mail_student.delay("nonexistent-id").result
    assert "not found" in result
    mock_send_email.assert_not_called()
