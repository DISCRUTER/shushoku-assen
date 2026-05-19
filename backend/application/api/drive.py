from http import HTTPStatus

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint, abort
from celery.result import AsyncResult

from application.tasks import drive_notification
from application.factory import db, role_required
from application.util_enum import DriveStatus
from application.models import Drive, CompanyDetails
from application.schema import DriveSchema, DriveListSchema, DriveUpdateSchema, DriveFilterSchema, DriveRegistrationSchema, ResponseSchema


drives = Blueprint('drives', __name__, url_prefix='/api/v1/drives', description="Endpoint to retrieve info about drives.")

@drives.route('/')
class Drives(MethodView):
    @jwt_required()
    @drives.arguments(DriveFilterSchema, location='query')
    @drives.response(HTTPStatus.OK, DriveListSchema(many=True))
    def get(self, args):
        query = db.select(Drive)

        if args.get('company_id'):
            company_id = f"%{args.get('company_id')}%"
            query = query.where(Drive.company_id.like(company_id))
        if args.get('title'):
            title = f"%{args.get('title')}%"
            query = query.where(Drive.title.ilike(title))
        if args.get('job_type'):
            query = query.where(Drive.job_type == args.get('job_type'))
        if args.get('status'):
            query = query.where(Drive.status == args.get('status'))
        
        try:
            all_drives = db.session.execute(query).scalars().all()
            return all_drives
        except Exception as e:
            print("::FETCHING DRIVE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch drive data.")

    @role_required("Company")
    @drives.arguments(DriveRegistrationSchema)
    @drives.response(HTTPStatus.CREATED, DriveListSchema)
    def post(self, drive_data):
        company = db.session.get(CompanyDetails, drive_data.company_id)
        if not company:
            abort(HTTPStatus.NOT_FOUND, message="Company not found.")
        
        try:
            drive_data.status = DriveStatus.PENDING
            db.session.add(drive_data)
            title = drive_data.title
            company_name = company.registered_name
            db.session.commit()
            res = drive_notification.delay(title, company_name)
            return drive_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING DRIVE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to create drive.")

@drives.route('/<string:drive_id>')
class DriveProfile(MethodView):
    @jwt_required()
    @drives.response(HTTPStatus.OK, DriveSchema)
    def get(self, drive_id):
        try:
            drive = db.session.get(Drive, drive_id)
            if not drive:
                abort(HTTPStatus.NOT_FOUND, message="Drive not found.")
            return drive
        except Exception as e:
            print("::FETCHING DRIVE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to fetch drive.")

    @role_required(["Admin", "Company"])
    @drives.arguments(DriveUpdateSchema)
    @drives.response(HTTPStatus.OK, DriveListSchema)
    def patch(self, drive_data, drive_id):
        drive = db.session.get(Drive, drive_id)
        if not drive:
            abort(HTTPStatus.NOT_FOUND, message="Drive not found.")
        
        for key, value in drive_data.items():
            setattr(drive, key, value)
        
        try:
            db.session.add(drive)
            db.session.commit()
            return drive
        except Exception as e:
            db.session.rollback()
            print("::UPDATING DRIVE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to update drive.")

    @role_required("Admin")
    @drives.response(HTTPStatus.ACCEPTED, ResponseSchema)
    def delete(self, drive_id):
        try:
            drive = db.session.get(Drive, drive_id)
            if not drive:
                abort(HTTPStatus.NOT_FOUND, message="Drive not found.")

            db.session.delete(drive)
            db.session.commit()
            return {'msg': "Drive deleted successfully."}
        except Exception as e:
            db.session.rollback()
            print("::DELETING DRIVE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to delete drive data.")