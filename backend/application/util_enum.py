import enum


class Role(enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    COMPANY = "company"

class Branch(enum.Enum):
    CSE = "Computer Science"
    IT = "Information Technology"
    ECE = "Electronics and Communication"
    EE = "Electrical"
    ME = "Mechanical"
    CE = "Civil"

class DegreeType(enum.Enum):
    BTECH = "B.Tech"
    MTECH = "M.Tech"

class CompanyStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class DriveStatus(enum.Enum):
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"
    REJECTED = "rejected"

class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    SELECTED = "selected"
    REJECTED = "rejected"
    OFFERED = "offered"

class Industry(enum.Enum):
    IT = "Information Technology"
    FINANCE = "Finance"
    MARKETING = "Marketing"
    SALES = "Sales"
    HR = "Human Resources"
    OTHER = "Other"

class JobType(enum.Enum):
    INTERNSHIP = "internship"
    PART_TIME = "part-time"
    FULL_TIME = "full-time"