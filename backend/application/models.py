import uuid
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from application.util_enum import CompanyStatus, DriveStatus, ApplicationStatus, JobType
from application.factory import db


# Base Model
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


#region Utility

# Role Model
class Role(BaseModel):
    __tablename__ = "roles"
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    users = db.relationship('User', backref='role', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Role: {self.name}>"

# Branch Model
class Branch(BaseModel):
    __tablename__ = "branches"
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    students = db.relationship('StudentDetails', backref='branch', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Branch: {self.name}>"

# Academic Degree Model
class AcademicDegree(BaseModel):
    __tablename__ = "academic_degrees"
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    students = db.relationship('StudentDetails', backref='academic_degree', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Academic Degree: {self.name}>"

# Industry Model 
class Industry(BaseModel):
    __tablename__ = "industries"
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    companies = db.relationship('CompanyDetails', backref='industry', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Industry: {self.name}>"

# Skill Model
class Skill(BaseModel):
    __tablename__ = "skills"
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Skill: {self.name}>"
student_skills = db.Table('student_skills',
    db.Column('student_id', db.String(32), db.ForeignKey('student_details.id', ondelete='CASCADE'), primary_key=True),                          
    db.Column('skill_id', db.String(32), db.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True)                    
)
skills_required = db.Table('skills_required',
    db.Column('drive_id', db.String(32), db.ForeignKey('drives.id', ondelete='CASCADE'), primary_key=True),                          
    db.Column('skill_id', db.String(32), db.ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True)                    
)

#endregion

#region User

# user model
class User(BaseModel):
    __tablename__ = "users"
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    blacklisted = db.Column(db.Boolean, nullable=False, default=False)

    role_id = db.Column(db.String(36), db.ForeignKey('roles.id', ondelete='CASCADE'))

    company_details = db.relationship('CompanyDetails', backref='user', lazy=False, cascade='all, delete-orphan', uselist=False)
    student_details = db.relationship('StudentDetails', backref='user', lazy=False, cascade='all, delete-orphan', uselist=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def details(self):
        if self.role.name == "Company":
            return self.company_details
        elif self.role.name == "Student":
            return self.student_details
        else:
            return None

    def __repr__(self) -> str:
        return f"<User: {self.username} | Role: {self.role.name}"
    
# details abstract model
class Details(db.Model):
    __abstract__ = True
    id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

# student detail model
class StudentDetails(Details): # miodify it further
    __tablename__ = "student_details"
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    about = db.Column(db.Text)
    github = db.Column(db.String)
    linkedin = db.Column(db.String)
    branch_id = db.Column(db.String(36), db.ForeignKey('branches.id', ondelete='CASCADE'))
    year = db.Column(db.Integer, nullable=False)
    academic_degree_id = db.Column(db.String(36), db.ForeignKey('academic_degrees.id', ondelete='CASCADE'))
    cgpa = db.Column(db.Numeric(3, 2), nullable=False)

    skills = db.relationship('Skill',secondary=student_skills , backref='students')
    applications = db.relationship('Application', backref='student', lazy=True, cascade='all, delete-orphan')
    placements = db.relationship('Placement', backref='student', lazy=True, cascade='all, delete-orphan')

# company details model
class CompanyDetails(Details):
    __tablename__ = "company_details"
    registered_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    industry_id = db.Column(db.String(36), db.ForeignKey('industries.id', ondelete='CASCADE'))
    location = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(80), nullable=False, unique=True)
    contact_phone = db.Column(db.String(25), nullable=False, unique=True)
    website = db.Column(db.String(50), nullable=False, unique=True)
    status = db.Column(db.Enum(CompanyStatus), nullable=False, default=CompanyStatus.PENDING)

    drives = db.relationship('Drive', backref='company', lazy=True, cascade='all, delete-orphan')
    placements = db.relationship('Placement', backref='company', lazy=True, cascade='all, delete-orphan')

#endregion

#region Operations

# Drive model
class Drive(BaseModel):
    __tablename__ = "drives"
    company_id = db.Column(db.String(36), db.ForeignKey('company_details.id', ondelete='CASCADE'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    openings = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    job_type = db.Column(db.Enum(JobType), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(DriveStatus), nullable=False)

    skills_required = db.relationship('Skill',secondary=skills_required , backref='drives')
    applications = db.relationship('Application', backref='drive', lazy=True, cascade='all, delete-orphan')
    placements = db.relationship('Placement', backref='drive', lazy=True, cascade='all, delete-orphan')

# application model
class Application(BaseModel):
    __tablename__ = "applications"
    drive_id = db.Column(db.String(36), db.ForeignKey('drives.id', ondelete='CASCADE'))
    student_id = db.Column(db.String(36), db.ForeignKey('student_details.id', ondelete='CASCADE'))
    status = db.Column(db.Enum(ApplicationStatus), nullable=False)

# Placement model
class Placement(BaseModel):
    __tablename__ = "placements"
    student_id = db.Column(db.String(36), db.ForeignKey('student_details.id', ondelete='CASCADE'))
    company_id = db.Column(db.String(36), db.ForeignKey('company_details.id', ondelete='CASCADE'))
    drive_id = db.Column(db.String(36), db.ForeignKey('drives.id', ondelete='CASCADE'))
    joining_date = db.Column(db.Date, nullable=False)

#endregion