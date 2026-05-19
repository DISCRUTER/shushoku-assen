from flask import url_for
from marshmallow import validate, fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from application.factory import db
from application.models import User, StudentDetails, CompanyDetails, Drive, Application, Placement, Role, Branch, AcademicDegree, Industry, Skill
from application.util_enum import ApplicationStatus, DriveStatus, JobType, CompanyStatus


class ResponseSchema(Schema):
    msg = fields.String()

#region Authentication

class UserLoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(required=True)

class UserLoginResponseSchema(Schema):
    user_id = fields.String(required=True)
    role = fields.String(required=True)
#endregion

#region Utils

class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

        dump_only = ("id",)
        exclude = ("users", "created_at", "updated_at")

class BranchSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Branch
        load_instance = True
        sqla_session = db.session

        dump_only = ("id",)
        exclude = ("students", "created_at", "updated_at")

class AcademicDegreeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AcademicDegree
        load_instance = True
        sqla_session = db.session

        dump_only = ("id",)
        exclude = ("students", "created_at", "updated_at")

class IndustrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Industry
        load_instance = True
        sqla_session = db.session

        dump_only = ("id",)
        exclude = ("companies", "created_at", "updated_at")

class SkillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        load_instance = True
        sqla_session = db.session

        exclude = ("created_at", "updated_at")

#endregion


#region User

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        sqla_session = db.session

        load_only = ("password",)
        dump_only = ("id", "created_at", "updated_at", "blacklisted")
        exclude = ("student_details", "company_details")
    
    email = fields.Email()
    password = fields.String(load_only=True)
    
#endregion

#region Student Details

class StudentRegisterSchema(UserSchema):
    class Meta(UserSchema.Meta):
        model = StudentDetails
        load_instance = False
        include_fk = True

        exclude = ("skills", "applications", "placements", "user", "role")

class StudentListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudentDetails
        include_fk = True

        exclude = ("skills", "applications", "placements")  
    branch = fields.Nested(BranchSchema)
    academic_degree = fields.Nested(AcademicDegreeSchema)
    user = fields.Nested(UserSchema)

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudentDetails
        include_fk = True

        exclude = ("applications", "placements")  
    branch = fields.Nested(BranchSchema)
    academic_degree = fields.Nested(AcademicDegreeSchema)
    skills = fields.List(fields.Nested(SkillSchema))
    user = fields.Nested(UserSchema)

class StudentFilterSchema(Schema):
    blacklisted = fields.Boolean()
    name = fields.String()
    branch_id = fields.List(fields.String())
    year = fields.Integer()
    academic_degree_id = fields.List(fields.String())

class StudentUpdateSchema(Schema):
    blacklisted = fields.Boolean()
    about = fields.String()
    github = fields.String()
    linkedin = fields.String()
    cgpa = fields.Float()

#endregion

#region Company Details

class CompanyRegisterSchema(UserSchema):
    class Meta(UserSchema.Meta):
        model = CompanyDetails
        load_instance = False
        include_fk = True

        exclude = ("drives", "placements", "user", "status", "role")

class CompanyDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CompanyDetails
        include_fk = True

        exclude = ("drives", "placements", "industry_id")
    industry = fields.Nested(IndustrySchema)
    user = fields.Nested(UserSchema)

class CompanyFilterSchema(Schema):
    blacklisted = fields.Boolean()
    name = fields.String()
    industry_id = fields.List(fields.String())
    status = fields.Enum(CompanyStatus, by_value=True)

class CompanyUpdateSchema(Schema):
    blacklisted = fields.Boolean()
    description = fields.String()
    location = fields.String()
    contact_phone = fields.String()
    contact_email = fields.String()
    website = fields.String()
    status = fields.Enum(CompanyStatus, by_value=True)
    
#endregion


#region Opertaives

class DriveSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Drive
        load_instance = True
        include_fk = True
        sqla_session = db.session
        dump_only = ("id", "created_at", "updated_at", "status")
    job_type = fields.Enum(JobType, by_value=True)
    status = fields.Enum(DriveStatus, by_value=True)
    company = fields.Nested(CompanyDetailSchema)
    skills_required = fields.List(fields.Nested(SkillSchema))

class DriveRegistrationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Drive
        load_instance = True
        include_fk = True
        sqla_session = db.session
        dump_only = ("id", "created_at", "updated_at", "status")
    job_type = fields.Enum(JobType, by_value=True)
    openings = fields.Integer(required=True, validate=validate.Range(min=1))
    title = fields.String(required=True, validate=validate.Length(min=5, max=100))
    skills_required = fields.List(fields.Nested(SkillSchema))

class DriveListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Drive
        load_instance = True
        include_fk = True
        sqla_session = db.session

        dump_only = ("id", "created_at", "updated_at", "status")
        exclude = ("skills_required", "applications", "placements")
    # Validation
    job_type = fields.Enum(JobType, by_value=True)
    status = fields.Enum(DriveStatus, by_value=True)

class DriveUpdateSchema(Schema):
    status = fields.Enum(DriveStatus, by_value=True)

class DriveFilterSchema(Schema):
    company_id = fields.String()
    title = fields.String()
    job_type = fields.Enum(JobType, by_value=True)
    status = fields.Enum(DriveStatus, by_value=True)


class ApplicationListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True
        include_fk = True
        sqla_session = db.session

        dump_only = ("id", "created_at", "updated_at", "status")

    status = fields.Enum(ApplicationStatus, by_value=True)

class ApplicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True
        include_fk = True
        sqla_session = db.session

        dump_only = ("id", "created_at", "updated_at", "status")
        exclude = ("drive_id", "student_id")
    drive = fields.Nested(DriveSchema)
    student = fields.Nested(StudentSchema)
    
class ApplicationUpdateSchema(Schema):
    status = fields.Enum(ApplicationStatus, by_value=True)

class ApplicationFilterSchema(Schema):
    student_id = fields.String(required=False)
    drive_id = fields.String(required=False)
    company_id = fields.String(required=False)


class PlacementListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Placement
        load_instance = True
        include_fk = True
        sqla_session = db.session

        dump_only = ("id", "created_at", "updated_at")

class PlacementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Placement
        load_instance = True
        include_fk = True
        sqla_session = db.session

        dump_only = ("id", "created_at", "updated_at")
        exclude = ("student_id", "drive_id", "company_id")
    student = fields.Nested(StudentListSchema)
    drive = fields.Nested(DriveListSchema)
    company = fields.Nested(CompanyDetailSchema)

class PlacementFilterSchema(Schema):
    student_id = fields.String()
    drive_id = fields.String()
    company_id = fields.String()

#endregion

#region Analytics

class AnalyticsSchema(Schema):
    data = fields.List(fields.Tuple((fields.String(), fields.Integer())), required=True, dump_only=True)


# For Student
class StudentAnalyticsFilterSchema(Schema):
    drive_id = fields.String()
    branch = fields.Boolean()
    academic_degree = fields.Boolean()
    all = fields.Boolean()

# For Company
class CompanyAnalyticsFilterSchema(Schema):
    all = fields.Boolean()

# For Drive
class DriveAnalyticsFilterSchema(Schema):
    all = fields.Boolean()
    by_status = fields.Boolean()
    by_company = fields.Boolean()
    company_id = fields.String()

# For Applications
class ApplicationsAnalyticsFilterSchema(Schema):
    all = fields.Boolean()
    by_status = fields.Boolean()
    student_id = fields.String()
    drive_id = fields.String()
    company_id = fields.String()

# For Placements
class PlacementAnalyticsFilterSchema(Schema):
    all = fields.Boolean()
    student_id = fields.String()
    company_id = fields.String()
    drive_id = fields.String()

#endregion