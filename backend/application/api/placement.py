from http import HTTPStatus

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from application.factory import db, role_required, cache
from application.models import Placement, StudentDetails, CompanyDetails, Drive
from application.schema import PlacementListSchema, PlacementFilterSchema, PlacementSchema


placements = Blueprint('placements', __name__, url_prefix='/api/v1/placements', description="Endpoints to retrieve placement offers.")

@placements.route('/')
class Placements(MethodView):
    @jwt_required()
    @placements.arguments(PlacementFilterSchema, location='query')
    @placements.response(HTTPStatus.OK, PlacementListSchema(many=True))
    def get(self, args):
        query = db.select(Placement)

        if args.get('student_id'):
            student_id = f"%{args.get('student_id')}%"
            query = query.where(Placement.student_id.like(student_id))
        if args.get('company_id'):
            company_id = f"%{args.get('company_id')}%"
            query = query.where(Placement.company_id.like(company_id))
        if args.get('drive_id'):
            drive_id = f"%{args.get('drive_id')}%"
            query = query.where(Placement.drive_id.like(drive_id))
        
        try:
            all_placements = db.session.execute(query).scalars().all()
            return all_placements
        except Exception as e:
            print("::FETCHING PLACEMENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to fetch placement data.")

    @role_required("Company")
    @placements.arguments(PlacementListSchema)
    @placements.response(HTTPStatus.CREATED, PlacementListSchema)
    def post(self, placement_data):
        student = db.session.get(StudentDetails, placement_data.student_id)
        company = db.session.get(CompanyDetails, placement_data.company_id)
        drive = db.session.get(Drive, placement_data.drive_id)
        if not student or not company or not drive:
            abort(HTTPStatus.NOT_FOUND, message="Student, Company or Drive not found.")

        try:
            db.session.add(placement_data)
            db.session.commit()
            return placement_data
        except Exception as e:
            print("::CREATING PLACEMENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to create placement.")

@placements.route('/<string:placement_id>')
class PlacementProfile(MethodView):
    @jwt_required()
    @cache.cached(timeout=10, query_string=True)
    @placements.response(HTTPStatus.OK, PlacementSchema)
    def get(self, placement_id):
        try:
            placement = db.session.get(Placement, placement_id)
            if not placement:
                abort(HTTPStatus.NOT_FOUND, message="Placement offer not found.")
            return placement
        except Exception as e:
            print("::FETCHING PLACEMENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to fetch placement offer.")