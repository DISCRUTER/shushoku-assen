import pytest
from marshmallow import ValidationError

from application.schema import (
    AnalyticsSchema,
    ApplicationUpdateSchema,
    CompanyFilterSchema,
    DriveRegistrationSchema,
    StudentUpdateSchema,
    UserLoginSchema,
)
from application.util_enum import ApplicationStatus, CompanyStatus, JobType


class TestUserLoginSchema:
    def test_valid_credentials_load(self):
        data = UserLoginSchema().load({"email": "user@example.com", "password": "secret"})
        assert data["email"] == "user@example.com"
        assert data["password"] == "secret"

    @pytest.mark.parametrize("payload", [
        {"email": "not-an-email", "password": "secret"},
        {"email": "user@example.com"},
        {"password": "secret"},
        {},
    ])
    def test_invalid_payloads_raise(self, payload):
        with pytest.raises(ValidationError):
            UserLoginSchema().load(payload)


class TestDriveRegistrationSchema:
    def base_payload(self, **overrides):
        payload = {
            "title": "SDE Intern",
            "description": "Great role",
            "openings": 5,
            "salary": 50000,
            "job_type": "internship",
            "deadline": "2030-01-31",
        }
        payload.update(overrides)
        return payload

    def test_valid_load_produces_drive_instance(self, app):
        result = DriveRegistrationSchema().load(self.base_payload())
        assert result.title == "SDE Intern"
        assert result.job_type == JobType.INTERNSHIP
        assert result.openings == 5

    def test_title_too_short_rejected(self, app):
        with pytest.raises(ValidationError) as excinfo:
            DriveRegistrationSchema().load(self.base_payload(title="abc"))
        assert "title" in excinfo.value.messages

    def test_openings_must_be_positive(self, app):
        with pytest.raises(ValidationError) as excinfo:
            DriveRegistrationSchema().load(self.base_payload(openings=0))
        assert "openings" in excinfo.value.messages

    def test_invalid_job_type_rejected(self, app):
        with pytest.raises(ValidationError):
            DriveRegistrationSchema().load(self.base_payload(job_type="volunteer"))

    def test_invalid_deadline_format_rejected(self, app):
        with pytest.raises(ValidationError):
            DriveRegistrationSchema().load(self.base_payload(deadline="31-01-2030"))


class TestUpdateSchemas:
    def test_student_update_accepts_partial_fields(self):
        data = StudentUpdateSchema().load({"about": "new about", "cgpa": 9.1})
        assert data["cgpa"] == 9.1

    def test_student_update_rejects_unknown_fields(self):
        with pytest.raises(ValidationError) as excinfo:
            StudentUpdateSchema().load({"hacker_field": "x"})
        assert "hacker_field" in excinfo.value.messages

    def test_application_update_status_enum_by_value(self):
        data = ApplicationUpdateSchema().load({"status": "shortlisted"})
        assert data["status"] == ApplicationStatus.SHORTLISTED

    def test_application_update_invalid_status(self):
        with pytest.raises(ValidationError):
            ApplicationUpdateSchema().load({"status": "teleported"})


class TestFilterSchemas:
    def test_company_filter_status_enum(self):
        data = CompanyFilterSchema().load({"status": "approved"}, partial=True)
        assert data["status"] == CompanyStatus.APPROVED

    def test_company_filter_invalid_status(self):
        with pytest.raises(ValidationError):
            CompanyFilterSchema().load({"status": "bogus"}, partial=True)


class TestAnalyticsSchema:
    def test_dumps_pairs_preserving_structure(self):
        dumped = AnalyticsSchema().dump({"data": [("Total", 5), ("CSE", 3)]})
        assert [tuple(pair) for pair in dumped["data"]] == [("Total", 5), ("CSE", 3)]

    def test_dumps_list_rows(self):
        dumped = AnalyticsSchema().dump({"data": [["Total", 5], ["CSE", 3]]})
        assert [tuple(pair) for pair in dumped["data"]] == [("Total", 5), ("CSE", 3)]
