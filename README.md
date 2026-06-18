# Shushoku Assen
A placement protal that stremlines the hiring process. Helping companies find best talent and students best opportunity.
> [!NOTE]
> This project is kind of like `Linkedin - Social Networking` for internal placements in college.  

## Highlights
- Daily activity tracking and habit logging
- Visualization dashboard using Chart.js
- Summary analytics with date filtering
- Responsive UI built with VueJS
- Secure password hashing and user session handling
- Browse live placement drives, apply to a drive with a single click
- Track every application and placement offers
- Post drives, shortlist candidates, and manage your entire recruitment pipeline in one place
- Weekly activity reports mailed to user
- On demand reports for users
- Google Chat notification when new drives open

## Endpoints & Models

### Entities
- Student: Who apply in the drives.
- Company: Who start the drives.
- Admin: Who approves the drives and registrations.

### Resources
- Drive: Campaign started by company, approved by Admin and participated by students.
- Application: Submitted by the students who apply to the drive.
- Placement: Offered to students who are selected.

### Entities & Resource Based Endpoint
- Role
    - **GET**/utils/roles : Get all roles. -> All
    - **POST**/utils/roles : Create a new role. -> Admin

- Branch
    - **GET**/utils/branches : Get all branches. -> All
    - **POST**/utils/branches : Create a new branch. -> Admin

- Academic Degree
    - **GET**/utils/academic_degrees : Get all academic degrees. -> All
    - **POST**/utils/academic_degrees : Create a new academic degree. -> Admin

- Industry
    - **GET**/utils/industries : Get all industries. -> All
    - **POST**/utils/industries : Create a new industry. -> Admin

- Skill
    - **GET**/utils/skills : Get all skills. -> All
    - **POST**/utils/skills : Create a new skill. -> Admin

- Student
    - **GET**/students : Get all students. -> Admin
    - **POST**/students : Register a student. -> Student
    - **GET**/students/student_id : Retrieve info about self. -> Admin, Company & Student
    - **PATCH**/students/student_id : Update the profile. -> Student & Admin
    - **DELETE**/student/student_id : Delete a student. -> Admin & Student

- Company
    - **GET**/company : Get all companies. -> Admin & Student
    - **POST**/company : Register a company -> Company
    - **GET**/company/company_id -> Retrieve info about a company. -> Admin, Student & Company
    - **PATCH**/company/company_id -> Update company info. -> Admin & Company
    - **DELETE**/company/company_id -> Update company info. -> Admin & Company

- Drive
    - **GET**/drives : Get all the drives. -> Company, Admin & Student
        - Student : Checks the profiles and shows relevent drives.
        - Company : Retrieves all the drives they are hosting.
        - Admin : All drives.
    - **POST**/drives : Create a drive. -> Company
    - **GET**/drives/drive_id : Retrieve info about a drive. -> Admin, Student & Company
        - Admin : Can access all the drives.
        - Student : Can access all but mostly relevant to them.
        - Company : Only drives they hosted.
    - **PATCH**/drives/drive_id : Update a drive info. -> Admin

- Application
    - **GET**/applications : Get all the applications -> Admin, Student & Company
        - Student : Retrieves only application of a particular student.
    - **POST**/applications : Submit an application for a a drive. -> Student
    - **GET**/applications/application_id : Get a particular application -> Admin, Student & Company
        - Admin : All applications.
        - Student : All the applications they submitted.
        - Company : Applications relevant to their drives.
    - **PATCH**/applications/application_id : Update the status of application -> Company & Admin

- Placement
    - **GET**/placements : Get all placement offers made. -> Admin
    - **POST**/placements : Offer a placement. -> Company
    - **GET**/placements/placement_id : Retrieve a placement offer. -> Admin, Student & Company
        - Admin : All placements offers.
        - Student : Placements offered to them.
        - Company : Placement they offered.

- Analytics
    - **GET**/analytics/summary : Get a summary of all the data. -> Admin
    - **GET**/analytics/students : Get student related analytics. -> Admin
    - **GET**/analytics/companies : Get company related analytics. -> Admin
    - **GET**/analytics/drives : Get drive related analytics. -> Admin & Company
    - **GET**/analytics/placements : Get placement related analytics. -> Admin

- Downloads
    - **GET**/report -> Admin only.
    - **GET**/student/student_id/report -> Admin, Student
    - **GET**/placement/placement_id/report -> All
    - **GET**/company/company_id/report -> Admin, Company
    - **GET**/drive/drive_id/report -> Admin, Company

### Models and Fields
- Base Model(Abstract)
    - ID
    - created_at
    - updated_at

#### Utility Models
- Role : Base Model
    - name
    - users -> one-many, List of users of that role
    - description

- Branch : Base Model
    - name
    - description
    - students -> one-many, list of all the students

- Academic Degree : Base Model
    - name
    - description
    - students -> one-many, list of all the students

- Industry : Base Model
    - name
    - description
    - companies -> one-many, list of all the companies

- Skills : Base Model
    - name
    - description

#### User Models
- User : Base Model
    - email
    - password
    - blacklisted
    - role -> FK:RoleName
    - Info -> one-one, Student:Student Details, Company:Company Details, role dependent

- Details(Abstract)
    - ID -> FK:UserID

- Student Details : Details
    - first_name
    - last_name
    - github
    - linkedin
    - branch -> FK:BranchID
    - year
    - academic_degree -> FK:AcademicDegreeID
    - cgpa
    - application -> one-many, List of all the application submitted by student, relation:Applications
    - placement -> one-many, List of all the placement offers, relation:Placements
    - skills -> many-many, list of all the skills student has, relation:Skills

- Company Details : Details
    - registered_name
    - description
    - industry -> FK:IndustryID
    - location
    - contact_email
    - contact_phone
    - website
    - status
    - drives -> one-many, list of all the drives hosted, relation:Drives
    - placements -> one-many, list of all the offers made, relation:Placements

#### Operational Models
- Drives : Base Model
    - company_id -> FK:Company
    - title
    - description
    - openings
    - salary
    - salary_type
    - deadline
    - status
    - skills_required -> many-many, list of all the skills required, relation:Skills
    - application -> one-many, list of all the application, relation:Applications
    - placements -> one-many, list of all the placement offers made., relation:Placements

- Applications : Base Model
    - drive_id -> FK:DriveID
    - student_id -> FK:StudentID
    - status

- Placements : Base Model
    - student_id -> FK:StudentID
    - company_id -> FK:CompanyID
    - drive_id -> FK:DriveID
    - joining_date
