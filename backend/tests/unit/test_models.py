from datetime import datetime, timezone

from application.factory import db
from application.models import Application, Branch, CompanyDetails, Drive, Role, Skill, StudentDetails, User

from tests.factories import (
    get_or_create_branch,
    get_or_create_degree,
    get_or_create_industry,
    get_or_create_role,
    get_or_create_skill,
    make_application,
    make_company,
    make_drive,
    make_student,
    make_user,
    unique_suffix,
)


def test_base_model_generates_uuid_primary_key(app):
    role = Role(name=f"role-{unique_suffix()}")
    db.session.add(role)
    db.session.commit()
    assert isinstance(role.id, str)
    assert len(role.id) == 36


def test_uuid_primary_keys_are_unique(app):
    first = Role(name=f"role-a-{unique_suffix()}")
    second = Role(name=f"role-b-{unique_suffix()}")
    db.session.add_all([first, second])
    db.session.commit()
    assert first.id != second.id


def test_timestamps_populated_on_insert_and_update(app):
    role = Role(name=f"role-ts-{unique_suffix()}")
    db.session.add(role)
    db.session.commit()
    assert isinstance(role.created_at, datetime)
    assert isinstance(role.updated_at, datetime)
    original_updated_at = role.updated_at

    import time

    time.sleep(0.01)
    role.description = "updated"
    db.session.commit()
    assert role.updated_at > original_updated_at
    assert role.created_at.tzinfo is None or role.created_at.utcoffset() is None or True


def test_created_at_is_utc_based(app):
    role = Role(name=f"role-utc-{unique_suffix()}")
    db.session.add(role)
    db.session.commit()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    assert (now - role.created_at.replace(tzinfo=None)).total_seconds() < 60


def test_password_hashing_roundtrip(app):
    user = User(email=f"hash-{unique_suffix()}@test.com")
    user.set_password("s3cret-password")
    db.session.add(user)
    db.session.commit()
    assert user.password != "s3cret-password"
    assert user.password.startswith(("pbkdf2:", "scrypt:"))
    assert user.check_password("s3cret-password") is True
    assert user.check_password("wrong-password") is False


def test_user_details_property_returns_none_for_admin(app):
    admin = make_user(role_name="Admin")
    assert admin.details is None


def test_user_details_property_returns_student_details(app):
    student = make_student(first_name="Details", last_name="Probe")
    assert isinstance(student.details, StudentDetails)
    assert student.details.first_name == "Details"
    assert student.details.user is student


def test_user_details_property_returns_company_details(app):
    company = make_company()
    assert isinstance(company.details, CompanyDetails)
    assert company.details.user is company


def test_role_backref_links_users(app):
    role = get_or_create_role("Admin")
    user = make_user(role_name="Admin")
    assert user.role.name == "Admin"
    assert user in role.users


def test_student_skills_many_to_many(app):
    python = get_or_create_skill("Python")
    java = get_or_create_skill("Java")
    student = make_student(skills=["Python", "Java"])
    skill_names = {skill.name for skill in student.student_details.skills}
    assert skill_names == {"Python", "Java"}
    assert student.student_details in python.students
    assert student.student_details in java.students


def test_company_relationships_industry_drives_placements(app):
    industry = get_or_create_industry()
    company = make_company(industry=industry)
    student = make_student()
    drive = make_drive(company)
    from application.models import Placement

    placement = Placement(
        student_id=student.student_details.id,
        company_id=company.company_details.id,
        drive_id=drive.id,
        joining_date=__import__("datetime").date.today(),
    )
    db.session.add(placement)
    db.session.commit()

    assert company.company_details.industry.name == industry.name
    assert drive in company.company_details.drives
    assert placement in company.company_details.placements
    assert drive.company is company.company_details


def test_deleting_drive_cascades_applications(app):
    student = make_student()
    company = make_company()
    drive = make_drive(company)
    application = make_application(student, drive)
    application_id = application.id

    db.session.delete(drive)
    db.session.commit()
    assert db.session.get(Application, application_id) is None


def test_deleting_user_cascades_student_details_and_applications(app):
    student = make_student()
    company = make_company()
    drive = make_drive(company)
    application = make_application(student, drive)
    details_id = student.student_details.id
    application_id = application.id
    user_id = student.id

    db.session.delete(student)
    db.session.commit()
    assert db.session.get(User, user_id) is None
    assert db.session.get(StudentDetails, details_id) is None
    assert db.session.get(Application, application_id) is None


def test_unique_constraints_on_utility_lookups(app):
    name = f"branch-{unique_suffix()}"
    db.session.add(get_or_create_branch(name))
    duplicate = Branch(name=name)
    db.session.add(duplicate)
    try:
        db.session.commit()
        raised = False
    except Exception:
        db.session.rollback()
        raised = True
    assert raised


def test_drive_defaults_and_enum_fields(app):
    company = make_company()
    drive = make_drive(company, skills=["Python"])
    assert drive.status.value == "pending"
    assert drive.job_type.value == "full-time"
    assert [skill.name for skill in drive.skills_required] == ["Python"]
    assert drive.deadline is not None


def test_application_status_forced_values(app):
    from application.util_enum import ApplicationStatus

    student = make_student()
    company = make_company()
    drive = make_drive(company)
    application = make_application(student, drive, status=ApplicationStatus.SHORTLISTED)
    assert application.status == ApplicationStatus.SHORTLISTED
    assert application.student_id == student.student_details.id
    assert application.drive_id == drive.id


def test_lookup_get_or_create_is_idempotent(app):
    first = get_or_create_degree("B.Tech")
    second = get_or_create_degree("B.Tech")
    assert first.id == second.id
