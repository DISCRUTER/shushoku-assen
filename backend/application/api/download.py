import os
from http import HTTPStatus

from flask import send_from_directory, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from celery.result import AsyncResult

from application.factory import role_required, db
from application.models import StudentDetails, CompanyDetails, Drive, Placement
from application.tasks import generate_admin_report, generate_student_report, generate_company_report, generate_drive_report, generate_placement_offer


downloads = Blueprint('downloads', __name__, url_prefix='/api/v1/downloads', description="Enpoint tom download resources.")


@downloads.route('/report')
class Report(MethodView):
    @role_required("Admin")
    def get(self):
        result = generate_admin_report.delay()
        return {
            "id": result.id
        }

@downloads.route('/student/<string:student_id>/report')
class StudentReport(MethodView):
    @role_required(["Admin", "Student"])
    def get(self, student_id):
        if not db.session.get(StudentDetails, student_id):
            abort(HTTPStatus.NOT_FOUND, message="Student not found.")
        result = generate_student_report.delay(student_id)
        return {
            "id": result.id
        }

@downloads.route('/company/<string:company_id>/report')
class CompanyReport(MethodView):
    @role_required(["Admin", "Company"])
    def get(self, company_id):
        if not db.session.get(CompanyDetails, company_id):
            abort(HTTPStatus.NOT_FOUND, message="Company not found.")
        result = generate_company_report.delay(company_id)
        return {
            "id": result.id
        }

@downloads.route('/drive/<string:drive_id>/report')
class DriveReport(MethodView):
    @role_required(["Admin", "Company"])
    def get(self, drive_id):
        if not db.session.get(Drive, drive_id):
            abort(HTTPStatus.NOT_FOUND, message="Drive not found.")
        result = generate_drive_report.delay(drive_id)
        return {
            "id": result.id
        }

@downloads.route('/placement/<string:placement_id>/report')
class PlacementReport(MethodView):
    @jwt_required()
    def get(self, placement_id):
        if not db.session.get(Placement, placement_id):
            abort(HTTPStatus.NOT_FOUND, message="Placement offer not found.")
        result = generate_placement_offer.delay(placement_id)
        return {
            "id": result.id
        }

@downloads.route('/<id>')
class Download(MethodView):
    @jwt_required()
    def get(self, id):
        res = AsyncResult(id)
        if not res.ready():
            return {'message': "Report is still generating."}, HTTPStatus.ACCEPTED
        if not res.successful() or not res.result:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Report generation failed.")
        
        reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
        return send_from_directory(reports_dir, res.result)