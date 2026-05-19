from http import HTTPStatus

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from application.factory import db, role_required
from application.util_enum import ApplicationStatus
from application.models import Application, StudentDetails, Drive
from application.schema import ApplicationListSchema, ApplicationUpdateSchema, ApplicationFilterSchema, ApplicationSchema

applications = Blueprint('applications', __name__, url_prefix='/api/v1/applications', description="Endpoint to retrieve info about applications.")

@applications.route('/')
class Applications(MethodView):
    @jwt_required()
    @applications.arguments(ApplicationFilterSchema, location='query')
    @applications.response(HTTPStatus.OK, ApplicationListSchema(many=True))
    def get(self, args):
        query = db.select(Application)

        if args.get('student_id'):
            student_id = f"%{args.get('student_id')}%"
            query = query.where(Application.student_id.like(student_id))
        if args.get('drive_id'):
            drive_id = f"%{args.get('drive_id')}%"
            query = query.where(Application.drive_id.like(drive_id))
        if args.get('company_id'):
            company_id = f"%{args.get('company_id')}%"
            query = query.join(Drive).where(Drive.company_id.like(company_id))
            
        try:
            all_applications = db.session.execute(query).scalars().all()
            return all_applications
        except Exception as e:
            print("::FETCHING APPLICATION::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch application data.")

    @role_required("Student")
    @applications.arguments(ApplicationListSchema)
    @applications.response(HTTPStatus.CREATED, ApplicationListSchema)
    def post(self, application_data):
        student = db.session.get(StudentDetails, application_data.student_id)
        drive = db.session.get(Drive, application_data.drive_id)
        if not student or not drive:
            abort(HTTPStatus.NOT_FOUND, message="Student or Drive not found.")
        
        try:
            application_data.status = ApplicationStatus.APPLIED
            db.session.add(application_data)
            db.session.commit()
            return application_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING APPLICATION::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to create application.")

@applications.route('/<string:application_id>')
class ApplicationProfile(MethodView):
    @jwt_required()
    @applications.response(HTTPStatus.OK, ApplicationSchema)
    def get(self, application_id):
        try:
            application = db.session.get(Application, application_id)
            if not application:
                abort(HTTPStatus.NOT_FOUND, message="Application not found.")
            return application
        except Exception as e:
            print("::FETCHING APPLICATION::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to fetch application.")

    @role_required(["Admin", "Company"])
    @applications.arguments(ApplicationUpdateSchema)
    @applications.response(HTTPStatus.OK, ApplicationListSchema)
    def patch(self, application_data, application_id):
        application = db.session.get(Application, application_id)
        if not application:
            abort(HTTPStatus.NOT_FOUND, message="Application not found.")
        
        for key, value in application_data.items():
            setattr(application, key, value)
        
        try:
            db.session.add(application)
            db.session.commit()
            return application
        except Exception as e:
            db.session.rollback()
            print("::UPDATING APPLICATION::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to update application.")