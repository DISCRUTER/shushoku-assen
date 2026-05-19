from datetime import datetime, timedelta
from application.factory import db
from application.models import *

#region Data

role = [
    {
        "name": "Admin",
        "description": "Superuser. Access to core functionalities."
    },
    {
        "name": "Student",
        "description": "User who will apply to drives."
    },
    {
        "name": "Company",
        "description": "Users who host drives."
    }
]

branch = [
    {
        "name": "Computer Science",
        "description": "Study of computation, automation, and information."
    },
    {
        "name": "Mechanical Engineering",
        "description": "Engineering branch that combines engineering physics and mathematics principles with materials science."
    },
    {
        "name": "Data Science",
        "description": "Field of study that combines domain expertise, programming skills, and knowledge of mathematics and statistics to extract meaningful insights from data."
    },
    {
        "name": "Civil Engineering",
        "description": "Professional engineering discipline that deals with the design, construction, and maintenance of the physical and naturally built environment."
    },
    {
        "name": "Aerospace and Aeronautical Engineering",
        "description": "Primary field of engineering concerned with the development of aircraft and spacecraft."
    }
]

academic_degree = [
    {"name": "BS", "description": "Bachelor of Science"},
    {"name": "MS", "description": "Master of Science"},
    {"name": "B.Tech", "description": "Bachelor of Technology"},
    {"name": "M.Tech", "description": "Master of Technology"},
    {"name": "Phd", "description": "Doctor of Philosophy"}
]

industry = [
    {
        "name": "Technology & AI",
        "description": "Sector focused on electronics, software, computers, artificial intelligence, and other related industries."
    },
    {
        "name": "Financial Services",
        "description": "Economic services provided by the finance industry."
    },
    {
        "name": "Retail & E-commerce",
        "description": "Sale of goods and services to consumers."
    },
    {
        "name": "Automotive",
        "description": "Wide range of companies and organizations involved in the design, development, manufacturing, marketing, and selling of motor vehicles."
    },
    {
        "name": "Manufacturing",
        "description": "Production of merchandise for use or sale using labour and machines, tools, chemical and biological processing, or formulation."
    },
    {
        "name": "EdTech",
        "description": "Combined use of computer hardware, software, and educational theory and practice to facilitate learning."
    },
    {
        "name": "Defense Manufacturing",
        "description": "Industry responsible for the design, development, production, and service of military weapons and systems."
    }
]

skill = [
    {"name": "Frontend Dev", "description": "Development of the graphical user interface of a website."},
    {"name": "Backend Dev", "description": "Server-side development."},
    {"name": "Fullstack Dev", "description": "Development of both client and server software."},
    {"name": "Machine Learning", "description": "Study of computer algorithms that improve automatically through experience."},
    {"name": "Deep Learning", "description": "Part of a broader family of machine learning methods based on artificial neural networks."},
    {"name": "Artificial Intelligence", "description": "Intelligence demonstrated by machines."},
    {"name": "Graphic Programming", "description": "Programming for computer graphics."},
    {"name": "Data Structures", "description": "Data organization, management, and storage format."},
    {"name": "Algorithms", "description": "Finite sequence of well-defined, computer-implementable instructions."},
    {"name": "Database Management Systems", "description": "System software for creating and managing databases."},
    {"name": "Android Dev", "description": "Software development for devices running the Android operating system."},
    {"name": "iOS Dev", "description": "Software development for devices running the iOS operating system."},
    {"name": "Python", "description": "High-level, general-purpose programming language."},
    {"name": "Java", "description": "Class-based, object-oriented programming language."},
    {"name": "Javascript", "description": "Programming language that is one of the core technologies of the World Wide Web."},
    {"name": "C", "description": "General-purpose, procedural computer programming language."}
]

admin = {
    "email": "user@admin.com",
    "password": "password"
}

students = [
    {
        "email": "user@student1.com",
        "password": "password",
        "first_name": "Student",
        "last_name": "One",
        "about": "I am student-I",
        "github": "www.fakegithub.com/one",
        "linkedin": "www.fakelinkedin.com/one",
        "branch": "Computer Science",
        "year": 2,
        "academic_degree": "B.Tech",
        "cgpa": 9.51,
        "skills": ["Python", "Java", "Data Structures"]
    },
    {
        "email": "user@student2.com",
        "password": "password",
        "first_name": "Student",
        "last_name": "Two",
        "about": "I am student-II",
        "github": "www.fakegithub.com/two",
        "linkedin": "www.fakelinkedin.com/two",
        "branch": "Data Science",
        "year": 3,
        "academic_degree": "BS",
        "cgpa": 8.54,
        "skills": ["Python", "Machine Learning", "Data Structures"]
    },
    {
        "email": "user@student3.com",
        "password": "password",
        "first_name": "Student",
        "last_name": "Three",
        "about": "I am student-III",
        "github": "www.fakegithub.com/three",
        "linkedin": "www.fakelinkedin.com/three",
        "branch": "Mechanical Engineering",
        "year": 4,
        "academic_degree": "B.Tech",
        "cgpa": 7.66,
        "skills": ["C", "Algorithms", "Data Structures"]
    }
]

companies = [
    {
        "email": "hr@techcorp.com",
        "password": "password",
        "registered_name": "Tech Corp",
        "description": "Leading tech company.",
        "industry": "Technology & AI",
        "location": "Silicon Valley",
        "contact_email": "contact@techcorp.com",
        "contact_phone": "1234567890",
        "website": "www.techcorp.com",
        "status": "approved"
    },
    {
        "email": "hr@financeltd.com",
        "password": "password",
        "registered_name": "Finance Ltd",
        "description": "Global financial services.",
        "industry": "Financial Services",
        "location": "New York",
        "contact_email": "contact@financeltd.com",
        "contact_phone": "0987654321",
        "website": "www.financeltd.com",
        "status": "pending"
    },
    {
        "email": "hr@badcompany.com",
        "password": "password",
        "registered_name": "Bad Company",
        "description": "Not a good company.",
        "industry": "Retail & E-commerce",
        "location": "Nowhere",
        "contact_email": "contact@badcompany.com",
        "contact_phone": "1122334455",
        "website": "www.badcompany.com",
        "status": "rejected"
    }
]

drives = [
    {
        "company_email": "hr@techcorp.com",
        "title": "SDE Intern",
        "description": "Software Development Engineer Intern role.",
        "openings": 5,
        "salary": 50000,
        "job_type": "internship",
        "deadline": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "status": "open",
        "skills_required": ["Python", "Data Structures", "Algorithms"]
    },
    {
        "company_email": "hr@techcorp.com",
        "title": "Full Stack Developer",
        "description": "Full time role for full stack developer.",
        "openings": 2,
        "salary": 1200000,
        "job_type": "full-time",
        "deadline": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "status": "closed",
        "skills_required": ["Fullstack Dev", "Javascript"]
    },
    {
        "company_email": "hr@financeltd.com",
        "title": "Analyst",
        "description": "Financial Analyst role.",
        "openings": 3,
        "salary": 800000,
        "job_type": "full-time",
        "deadline": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
        "status": "pending",
        "skills_required": ["Python"]
    },
    {
        "company_email": "hr@badcompany.com",
        "title": "Frontend Intern",
        "description": "Frontend development internship.",
        "openings": 4,
        "salary": 20000,
        "job_type": "internship",
        "deadline": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
        "status": "open",
        "skills_required": ["Frontend Dev", "Javascript"]
    },
    {
        "company_email": "hr@techcorp.com",
        "title": "Part-time Tester",
        "description": "Manual testing of applications.",
        "openings": 2,
        "salary": 15000,
        "job_type": "part-time",
        "deadline": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "status": "open",
        "skills_required": ["Java"]
    }
]

applications = [
    {"student_email": "user@student1.com", "drive_title": "SDE Intern", "company_email": "hr@techcorp.com", "status": "offered"},
    {"student_email": "user@student2.com", "drive_title": "SDE Intern", "company_email": "hr@techcorp.com", "status": "shortlisted"},
    {"student_email": "user@student1.com", "drive_title": "Full Stack Developer", "company_email": "hr@techcorp.com", "status": "rejected"},
    {"student_email": "user@student2.com", "drive_title": "Full Stack Developer", "company_email": "hr@techcorp.com", "status": "selected"},
    {"student_email": "user@student3.com", "drive_title": "Full Stack Developer", "company_email": "hr@techcorp.com", "status": "applied"}
]

placements = [
    {"student_email": "user@student1.com", "company_email": "hr@techcorp.com", "drive_title": "SDE Intern", "joining_date": "2024-06-01"}
]

#endregion

def data_creation():

    print("Creating database...")
    db.create_all()
    print("Database created successfully!")

    # Role
    def get_or_create_role(role_data):
        role = db.session.execute(db.select(Role).filter_by(name=role_data["name"])).scalar_one_or_none()
        if not role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"]
            )
            db.session.add(role)
        return role
    
    print("Propagating Roles...")
    try:
        roles_data = {}
        for roles in role:
            roles_data[roles['name']] = get_or_create_role(roles)
        db.session.commit()
        print("Roles added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred propagating roles: {str(e)}")
        return
    
    # Branch
    def get_or_create_branch(branch_data):
        branch = db.session.execute(db.select(Branch).filter_by(name=branch_data["name"])).scalar_one_or_none()
        if not branch:
            branch = Branch(
                name=branch_data["name"],
                description=branch_data["description"]
            )
            db.session.add(branch)
        return branch
    
    print("Propagating Branches...")
    try:
        branch_data = {}
        for branches in branch:
            branch_data[branches['name']] = get_or_create_branch(branches)
        db.session.commit()
        print("Branches added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred propagating branches: {str(e)}")
        return

    # Academic Degree
    def get_or_create_degree(degree_item):
        degree = db.session.execute(db.select(AcademicDegree).filter_by(name=degree_item["name"])).scalar_one_or_none()
        if not degree:
            degree = AcademicDegree(
                name=degree_item["name"],
                description=degree_item["description"]
            )
            db.session.add(degree)
        return degree
    
    print("Propagating Academic Degrees...")
    try:
        degree_data = {}
        for degree in academic_degree:
            degree_data[degree['name']] = get_or_create_degree(degree)
        db.session.commit()
        print("Academic Degrees added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred propagating academic degrees: {str(e)}")
        return

    # Industry
    def get_or_create_industry(industry_item):
        ind = db.session.execute(db.select(Industry).filter_by(name=industry_item["name"])).scalar_one_or_none()
        if not ind:
            ind = Industry(
                name=industry_item["name"],
                description=industry_item["description"]
            )
            db.session.add(ind)
        return ind
    
    print("Propagating Industries...")
    try:
        industry_data = {}
        for ind in industry:
            industry_data[ind['name']] = get_or_create_industry(ind)
        db.session.commit()
        print("Industries added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred propagating industries: {str(e)}")
        return

    # Skill
    def get_or_create_skill(skill_item):
        sk = db.session.execute(db.select(Skill).filter_by(name=skill_item["name"])).scalar_one_or_none()
        if not sk:
            sk = Skill(
                name=skill_item["name"],
                description=skill_item["description"]
            )
            db.session.add(sk)
        return sk
    
    print("Propagating Skills...")
    try:
        skill_data = {}
        for sk in skill:
            skill_data[sk['name']] = get_or_create_skill(sk)
        db.session.commit()
        print("Skills added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred propagating skills: {str(e)}")
        return

    # Admin
    print("Creating Admin...")
    try:
        if not db.session.execute(db.select(User).filter_by(email=admin["email"])).scalar_one_or_none():
            u = User(email=admin["email"], role=roles_data["Admin"])
            u.set_password(admin["password"])
            db.session.add(u)
            db.session.commit()
            print("Admin created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred creating admin: {str(e)}")

    # Students
    print("Creating Students...")
    try:
        for s in students:
            if not db.session.execute(db.select(User).filter_by(email=s["email"])).scalar_one_or_none():
                u = User(email=s["email"], role=roles_data["Student"])
                u.set_password(s["password"])
                db.session.add(u)
                db.session.flush()
                
                sd = StudentDetails(
                    id=u.id,
                    first_name=s["first_name"],
                    last_name=s["last_name"],
                    about=s["about"],
                    github=s["github"],
                    linkedin=s["linkedin"],
                    branch=branch_data[s["branch"]],
                    year=s["year"],
                    academic_degree=degree_data[s["academic_degree"]],
                    cgpa=s["cgpa"]
                )
                for sk in s["skills"]:
                    sd.skills.append(skill_data[sk])
                db.session.add(sd)
        db.session.commit()
        print("Students created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred creating students: {str(e)}")

    # Companies
    print("Creating Companies...")
    try:
        for c in companies:
            if not db.session.execute(db.select(User).filter_by(email=c["email"])).scalar_one_or_none():
                u = User(email=c["email"], role=roles_data["Company"])
                u.set_password(c["password"])
                db.session.add(u)
                db.session.flush()
                
                cd = CompanyDetails(
                    id=u.id,
                    registered_name=c["registered_name"],
                    description=c["description"],
                    industry=industry_data[c["industry"]],
                    location=c["location"],
                    contact_email=c["contact_email"],
                    contact_phone=c["contact_phone"],
                    website=c["website"],
                    status=CompanyStatus(c["status"])
                )
                db.session.add(cd)
        db.session.commit()
        print("Companies created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred creating companies: {str(e)}")

    # Drives
    print("Creating Drives...")
    try:
        for d in drives:
            comp_user = db.session.execute(db.select(User).filter_by(email=d["company_email"])).scalar_one()
            comp = comp_user.company_details
            
            if not db.session.execute(db.select(Drive).filter_by(title=d["title"], company_id=comp.id)).scalar_one_or_none():
                dr = Drive(
                    company_id=comp.id,
                    title=d["title"],
                    description=d["description"],
                    openings=d["openings"],
                    salary=d["salary"],
                    job_type=JobType(d["job_type"]),
                    deadline=datetime.strptime(d["deadline"], "%Y-%m-%d").date(),
                    status=DriveStatus(d["status"])
                )
                for sk in d["skills_required"]:
                    dr.skills_required.append(skill_data[sk])
                db.session.add(dr)
        db.session.commit()
        print("Drives created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred creating drives: {str(e)}")

    # Applications
    print("Creating Applications...")
    try:
        for a in applications:
            stu = db.session.execute(db.select(User).filter_by(email=a["student_email"])).scalar_one().student_details
            comp = db.session.execute(db.select(User).filter_by(email=a["company_email"])).scalar_one().company_details
            drv = db.session.execute(db.select(Drive).filter_by(title=a["drive_title"], company_id=comp.id)).scalar_one()
            
            if not db.session.execute(db.select(Application).filter_by(student_id=stu.id, drive_id=drv.id)).scalar_one_or_none():
                app = Application(
                    student_id=stu.id,
                    drive_id=drv.id,
                    status=ApplicationStatus(a["status"])
                )
                db.session.add(app)
        db.session.commit()
        print("Applications created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred creating applications: {str(e)}")

    # Placements
    print("Creating Placements...")
    try:
        for p in placements:
            stu = db.session.execute(db.select(User).filter_by(email=p["student_email"])).scalar_one().student_details
            comp = db.session.execute(db.select(User).filter_by(email=p["company_email"])).scalar_one().company_details
            drv = db.session.execute(db.select(Drive).filter_by(title=p["drive_title"], company_id=comp.id)).scalar_one()
            
            if not db.session.execute(db.select(Placement).filter_by(student_id=stu.id, drive_id=drv.id)).scalar_one_or_none():
                pl = Placement(
                    student_id=stu.id,
                    company_id=comp.id,
                    drive_id=drv.id,
                    joining_date=datetime.strptime(p["joining_date"], "%Y-%m-%d").date()
                )
                db.session.add(pl)
        db.session.commit()
        print("Placements created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred creating placements: {str(e)}")
