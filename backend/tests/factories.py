import uuid
from datetime import date, timedelta

from application.factory import db
from application.models import (
    AcademicDegree,
    Application,
    Branch,
    CompanyDetails,
    Drive,
    Industry,
    Placement,
    Role,
    Skill,
    StudentDetails,
    User,
)
from application.util_enum import (
    ApplicationStatus,
    CompanyStatus,
    DriveStatus,
    JobType,
)

DEFAULT_PASSWORD = "password"


def unique_suffix():
    return uuid.uuid4().hex[:10]


def get_or_create_role(name):
    role = db.session.execute(db.select(Role).filter_by(name=name)).scalar_one_or_none()
    if not role:
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
    return role


def get_role(name):
    return db.session.execute(db.select(Role).filter_by(name=name)).scalar_one()


def get_or_create_branch(name="Computer Science"):
    branch = db.session.execute(db.select(Branch).filter_by(name=name)).scalar_one_or_none()
    if not branch:
        branch = Branch(name=name)
        db.session.add(branch)
        db.session.commit()
    return branch


def get_or_create_degree(name="B.Tech"):
    degree = db.session.execute(db.select(AcademicDegree).filter_by(name=name)).scalar_one_or_none()
    if not degree:
        degree = AcademicDegree(name=name)
        db.session.add(degree)
        db.session.commit()
    return degree


def get_or_create_industry(name="Information Technology"):
    industry = db.session.execute(db.select(Industry).filter_by(name=name)).scalar_one_or_none()
    if not industry:
        industry = Industry(name=name)
        db.session.add(industry)
        db.session.commit()
    return industry


def get_or_create_skill(name):
    skill = db.session.execute(db.select(Skill).filter_by(name=name)).scalar_one_or_none()
    if not skill:
        skill = Skill(name=name)
        db.session.add(skill)
        db.session.commit()
    return skill


def ensure_base_lookups():
    for role_name in ("Admin", "Student", "Company"):
        get_or_create_role(role_name)
    get_or_create_branch("Computer Science")
    get_or_create_branch("Mechanical Engineering")
    get_or_create_degree("B.Tech")
    get_or_create_degree("M.Tech")
    get_or_create_industry("Information Technology")
    get_or_create_industry("Finance")
    for skill_name in ("Python", "Java", "Data Structures"):
        get_or_create_skill(skill_name)
    db.session.commit()


def make_user(email=None, role_name="Student", password=DEFAULT_PASSWORD, blacklisted=False):
    user = User(email=email or f"{unique_suffix()}@test.com", blacklisted=blacklisted)
    user.role = get_role(role_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def make_student(email=None, password=DEFAULT_PASSWORD, skills=None, **details):
    user = User(email=email or f"student_{unique_suffix()}@test.com")
    user.role = get_role("Student")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    student_details = StudentDetails(
        id=user.id,
        first_name=details.pop("first_name", "Test"),
        last_name=details.pop("last_name", "Student"),
        year=details.pop("year", 3),
        cgpa=details.pop("cgpa", 8.5),
        branch=details.pop("branch", None) or get_or_create_branch(),
        academic_degree=details.pop("academic_degree", None) or get_or_create_degree(),
        **details,
    )
    user.student_details = student_details
    db.session.add(student_details)
    db.session.flush()
    for skill_name in skills or []:
        student_details.skills.append(get_or_create_skill(skill_name))
    db.session.commit()
    return user


def make_company(
    status=CompanyStatus.APPROVED,
    industry=None,
    password=DEFAULT_PASSWORD,
    email=None,
    **details,
):
    suffix = unique_suffix()
    user = User(email=email or f"company_{suffix}@test.com")
    user.role = get_role("Company")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    company_details = CompanyDetails(
        id=user.id,
        registered_name=details.pop("registered_name", f"Test Corp {suffix}"),
        description=details.pop("description", "A test company."),
        location=details.pop("location", "Test City"),
        contact_email=details.pop("contact_email", f"contact_{suffix}@testcorp.com"),
        contact_phone=details.pop("contact_phone", str(9000000000 + (uuid.uuid4().int % 999999999))),
        website=details.pop("website", f"https://www.test{suffix}.com"),
        industry=industry or get_or_create_industry(),
        status=status,
        **details,
    )

    user.company_details = company_details
    db.session.add(company_details)
    db.session.commit()
    return user


def make_drive(
    company_user,
    status=DriveStatus.PENDING,
    job_type=JobType.FULL_TIME,
    deadline=None,
    skills=None,
    **details,
):
    drive = Drive(
        company_id=company_user.company_details.id,
        title=details.pop("title", f"Test Drive {unique_suffix()}"),
        description=details.pop("description", "A test drive."),
        openings=details.pop("openings", 3),
        salary=details.pop("salary", 50000),
        job_type=job_type,
        deadline=deadline or date.today() + timedelta(days=30),
        status=status,
        **details,
    )
    for skill_name in skills or []:
        drive.skills_required.append(get_or_create_skill(skill_name))
    db.session.add(drive)
    db.session.commit()
    return drive


def make_application(student_user, drive, status=ApplicationStatus.APPLIED):
    application = Application(
        student_id=student_user.student_details.id,
        drive_id=drive.id,
        status=status,
    )
    db.session.add(application)
    db.session.commit()
    return application


def make_placement(student_user, company_user, drive, joining_date=None):
    placement = Placement(
        student_id=student_user.student_details.id,
        company_id=company_user.company_details.id,
        drive_id=drive.id,
        joining_date=joining_date or date.today() + timedelta(days=60),
    )
    db.session.add(placement)
    db.session.commit()
    return placement
