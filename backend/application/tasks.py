import os
import httpx
from datetime import datetime
from celery import shared_task
from flask import render_template, current_app
from weasyprint import HTML
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import or_

from application.mail import send_email
from application.factory import db
from application.models import Drive, CompanyDetails, StudentDetails, Application, Placement
from application.util_enum import DriveStatus


@shared_task(ignore_results=False, name="Admin Report")
def generate_admin_report(): 
    try:
        company_data = db.session.execute(
            db.select(CompanyDetails).options(
                joinedload(CompanyDetails.user),
                joinedload(CompanyDetails.industry)
            )
        ).scalars().all()
        student_data = db.session.execute(
            db.select(StudentDetails).options(
                joinedload(StudentDetails.user),
                joinedload(StudentDetails.branch),
                joinedload(StudentDetails.academic_degree)
            )
        ).scalars().all()
        drive_data = db.session.execute(
            db.select(Drive).options(
                selectinload(Drive.skills_required),
                joinedload(Drive.company),
                selectinload(Drive.applications).joinedload(Application.student),
                selectinload(Drive.placements).joinedload(Placement.student)
            )
        ).scalars().all()

        html_out = render_template("report.html", company_data=company_data, student_data=student_data, drive_data=drive_data)
        
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        pdf_filename = f"report_admin_{int(datetime.now().timestamp())}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
    
        HTML(string=html_out).write_pdf(pdf_path)

        return pdf_filename
    except Exception as e:
        print(f"Error generating admin report: {e}")
        return None

@shared_task(ignore_results=False, name="Student Report")
def generate_student_report(student_id: str):
    try:
        student = db.session.execute(
            db.select(StudentDetails)
            .where(StudentDetails.id == student_id)
            .options(
                joinedload(StudentDetails.user),
                joinedload(StudentDetails.branch),
                joinedload(StudentDetails.academic_degree)
            )
        ).scalar_one_or_none()

        if not student:
            return "Student not found."

        stmt = (
            db.select(Drive)
            .outerjoin(Application, Drive.id == Application.drive_id)
            .outerjoin(Placement, Drive.id == Placement.drive_id)
            .where(or_(Application.student_id == student_id, Placement.student_id == student_id))
            .options(
                selectinload(Drive.skills_required),
                joinedload(Drive.company).options(
                    joinedload(CompanyDetails.user),
                    joinedload(CompanyDetails.industry)
                ),
                selectinload(Drive.applications).joinedload(Application.student),
                selectinload(Drive.placements).joinedload(Placement.student)
            )
        )
        drive_data = db.session.execute(stmt).scalars().unique().all()
        company_data = list({d.company for d in drive_data})

        html_out = render_template("report.html", student_data=[student], drive_data=drive_data, company_data=company_data)
        
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        pdf_filename = f"report_student_{student_id}_{int(datetime.now().timestamp())}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
    
        HTML(string=html_out).write_pdf(pdf_path)

        return pdf_filename
    except Exception as e:
        print(f"Error generating student report: {e}")
        return None

@shared_task(ignore_results=False, name="Company Report")
def generate_company_report(company_id: str):
    try:
        company = db.session.execute(
            db.select(CompanyDetails)
            .where(CompanyDetails.id == company_id)
            .options(joinedload(CompanyDetails.user), joinedload(CompanyDetails.industry))
        ).scalar_one_or_none()

        if not company:
            return "Company not found."

        stmt = (
            db.select(Drive)
            .where(Drive.company_id == company_id)
            .options(
                selectinload(Drive.skills_required),
                joinedload(Drive.company),
                selectinload(Drive.applications).joinedload(Application.student).options(
                    joinedload(StudentDetails.user), joinedload(StudentDetails.branch), joinedload(StudentDetails.academic_degree)
                ),
                selectinload(Drive.placements).joinedload(Placement.student).options(
                    joinedload(StudentDetails.user), joinedload(StudentDetails.branch), joinedload(StudentDetails.academic_degree)
                )
            )
        )
        drive_data = db.session.execute(stmt).scalars().all()

        students = set()
        for d in drive_data:
            for app in d.applications:
                students.add(app.student)
            for p in d.placements:
                students.add(p.student)
        
        html_out = render_template("report.html", company_data=[company], drive_data=drive_data, student_data=list(students))
        
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        pdf_filename = f"report_company_{company_id}_{int(datetime.now().timestamp())}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
    
        HTML(string=html_out).write_pdf(pdf_path)

        return pdf_filename
    except Exception as e:
        print(f"Error generating company report: {e}")
        return None

@shared_task(ignore_results=False, name="Drive Report")
def generate_drive_report(drive_id: str):
    try:
        stmt = (
            db.select(Drive)
            .where(Drive.id == drive_id)
            .options(
                selectinload(Drive.skills_required),
                joinedload(Drive.company).options(
                    joinedload(CompanyDetails.user),
                    joinedload(CompanyDetails.industry)
                ),
                selectinload(Drive.applications).joinedload(Application.student),
                selectinload(Drive.placements).joinedload(Placement.student)
            )
        )
        drive = db.session.execute(stmt).scalar_one_or_none()

        if not drive:
            return "Drive not found."

        # Only passing drive_data as requested
        html_out = render_template("report.html", drive_data=[drive])
        
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        pdf_filename = f"report_drive_{drive_id}_{int(datetime.now().timestamp())}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
    
        HTML(string=html_out).write_pdf(pdf_path)

        return pdf_filename
    except Exception as e:
        print(f"Error generating drive report: {e}")
        return None

@shared_task(ignore_results=False, name="Placement Offer")
def generate_placement_offer(placement_id: str):
    try:
        placement = db.session.execute(
            db.select(Placement)
            .where(Placement.id == placement_id)
            .options(
                joinedload(Placement.company),
                joinedload(Placement.student),
                joinedload(Placement.drive)
            )
        ).scalar_one_or_none()

        if not placement:
            return "Placement not found."

        html_out = render_template("placement.html", placement=placement)
        
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        pdf_filename = f"placement_offer_{placement_id}_{int(datetime.now().timestamp())}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
    
        HTML(string=html_out).write_pdf(pdf_path)

        return pdf_filename
    except Exception as e:
        print(f"Error generating placement offer: {e}")
        return None


#region Routine Task

@shared_task(ignore_results=False, name="Drive Cleanup")
def drives_cleanup():
    try:
        drives = db.session.execute(db.select(Drive).where(Drive.status == DriveStatus.OPEN)).scalars().all()
        for drive in drives:
            if drive.deadline < datetime.now().date():
                drive.status = DriveStatus.CLOSED
        
        db.session.commit()
        return "Drive cleanup completed."
    except Exception as e:
        db.session.rollback()
        return f"Error during cleanup: {str(e)}"

@shared_task(ignore_results=False, name="Cron Checkup")
def cron_checkup():
    text = "Crontab testing"
    url = "https://chat.googleapis.com/v1/spaces/AAQAY3Ls2oQ/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=N_oNfbOy7957ubOBEKjClwJeUaWhNEL8EyLZzORVl8Q"
    try:
        response = httpx.post(url, json={"text": text})
        response.raise_for_status()
        print(response.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    return "The message is sent."

#endregion

#region Webhook Tasks

@shared_task(ignore_results=False, name="Drive Notification")
def drive_notification(drive_title, company_name):
    text = f"{company_name} has started drive for {drive_title}. Apply now http://127.0.0.1:5173"
    url = "Your google chat api key"
    try:
        response = httpx.post(url, json={"text": text})
        response.raise_for_status()
        print(response.json())
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    return "The message is sent."

#endregion

#region Mailing Task

@shared_task(ignore_results=False, name="Mail Student")
def mail_student(student_id: str):
    try:
        student = db.session.execute(
            db.select(StudentDetails)
            .where(StudentDetails.id == student_id)
            .options(joinedload(StudentDetails.user))
        ).scalar_one_or_none()

        if not student:
            return f"Student {student_id} not found."

        pdf_filename = generate_student_report(student_id)
        if not pdf_filename:
            return f"Failed to generate report for student {student_id}."

        pdf_path = os.path.join(current_app.root_path, 'static', 'reports', pdf_filename)
        recipient_email = student.user.email
        student_name = f"{student.first_name} {student.last_name or ''}".strip()

        subject = "Your Placement Report"
        message = (
            f"<p>Dear {student_name},</p>"
            f"<p>Please find attached your placement activity report.</p>"
            f"<p>This report contains a summary of the drives you applied to and your placement status.</p>"
            f"<br><p>Regards,<br>Shushoku Assen</p>"
        )

        send_email(
            to_address=recipient_email,
            subject=subject,
            message=message,
            content="html",
            attachment_file=pdf_path
        )

        return f"Report emailed successfully to {recipient_email}."
    except Exception as e:
        print(f"Error in mail_student for {student_id}: {e}")
        return f"Error: {str(e)}"


@shared_task(ignore_results=False, name="Mail Company")
def mail_company(company_id: str):
    try:
        company = db.session.execute(
            db.select(CompanyDetails)
            .where(CompanyDetails.id == company_id)
            .options(joinedload(CompanyDetails.user))
        ).scalar_one_or_none()

        if not company:
            return f"Company {company_id} not found."

        pdf_filename = generate_company_report(company_id)
        if not pdf_filename:
            return f"Failed to generate report for company {company_id}."

        pdf_path = os.path.join(current_app.root_path, 'static', 'reports', pdf_filename)
        recipient_email = company.contact_email
        company_name = company.registered_name

        subject = "Your Company Placement Report"
        message = (
            f"<p>Dear {company_name} Team,</p>"
            f"<p>Please find attached the placement report for your company.</p>"
            f"<p>This report includes details on your active drives, applications received, and confirmed placements.</p>"
            f"<br><p>Regards,<br>Shushoku Assen</p>"
        )

        send_email(
            to_address=recipient_email,
            subject=subject,
            message=message,
            content="html",
            attachment_file=pdf_path
        )

        return f"Report emailed successfully to {recipient_email}."
    except Exception as e:
        print(f"Error in mail_company for {company_id}: {e}")
        return f"Error: {str(e)}"


@shared_task(ignore_results=False, name="Mail All Students")
def mail_all_students():
    try:
        students = db.session.execute(db.select(StudentDetails)).scalars().all()
        dispatched = 0
        for student in students:
            mail_student.delay(student.id)
            dispatched += 1
        return f"Dispatched report emails for {dispatched} student(s)."
    except Exception as e:
        print(f"Error in mail_all_students: {e}")
        return f"Error: {str(e)}"


@shared_task(ignore_results=False, name="Mail All Companies")
def mail_all_companies():
    try:
        companies = db.session.execute(db.select(CompanyDetails)).scalars().all()
        dispatched = 0
        for company in companies:
            mail_company.delay(company.id)
            dispatched += 1
        return f"Dispatched report emails for {dispatched} company/companies."
    except Exception as e:
        print(f"Error in mail_all_companies: {e}")
        return f"Error: {str(e)}"


#endregion
