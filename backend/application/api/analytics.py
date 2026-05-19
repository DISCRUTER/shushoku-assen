from http import HTTPStatus

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from application.factory import db, cache
from application.models import CompanyDetails, StudentDetails, Drive, Application, Placement, Branch, AcademicDegree, Industry
from application.schema import AnalyticsSchema, StudentAnalyticsFilterSchema, DriveAnalyticsFilterSchema, ApplicationsAnalyticsFilterSchema, CompanyAnalyticsFilterSchema, PlacementAnalyticsFilterSchema


analytics = Blueprint('analytics', __name__, url_prefix='/api/v1/analytics', description="Endpoints to retrieve analytics.")

@analytics.route('/students')
class StudentAnaytic(MethodView):
    @jwt_required()
    @analytics.arguments(StudentAnalyticsFilterSchema, location='query')
    @cache.cached(timeout=10, query_string=True)
    @analytics.response(HTTPStatus.OK, AnalyticsSchema)
    def get(self, args):
        query = None
        if args.get('all'):
            query = db.select(db.func.count(StudentDetails.id))
        elif args.get('academic_degree'):
            query = db.select(
                AcademicDegree.name,
                db.func.count(StudentDetails.id)
            ).join(StudentDetails).group_by(AcademicDegree.id)
        else:
            query = db.select(
                Branch.name,
                db.func.count(StudentDetails.id)
            ).join(StudentDetails).group_by(Branch.id)
        
        try:
            results = db.session.execute(query).all()
            if args.get('all'):
                return {'data': [("Total", results[0][0])]}
            return {'data': results}
        except Exception as e:
            print("::FETCHING STUDENT ANALYTICS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch student analytics.")


@analytics.route('/company')
class CompanyAnalytics(MethodView):
    @jwt_required()
    @analytics.arguments(CompanyAnalyticsFilterSchema, location='query')
    @cache.cached(timeout=10, query_string=True)
    @analytics.response(HTTPStatus.OK, AnalyticsSchema)
    def get(self, args):
        query = None
        if args.get('all'):
            query = db.select(db.func.count(CompanyDetails.id))
        else:
            query = db.select(
                Industry.name,
                db.func.count(CompanyDetails.id)
            ).join(CompanyDetails).group_by(Industry.id)

        try:
            result = db.session.execute(query).all()
            if args.get('all'):
                return {'data': [("Total", result[0][0])]}
            return {'data': result}
        except Exception as e:
            print("::FETCHING COMPANY ANALYTICS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch company analytics.")

@analytics.route('/drives')
class DriveAnalytics(MethodView):
    @jwt_required()
    @analytics.arguments(DriveAnalyticsFilterSchema, location='query')
    @cache.cached(timeout=10, query_string=True)
    @analytics.response(HTTPStatus.OK, AnalyticsSchema)
    def get(self , args):
        query = None
        if args.get('all'):
            query = db.select(db.func.count(Drive.id))
        elif args.get('by_status'):
            query = db.select(
                Drive.status,
                db.func.count(Drive.id)
            ).group_by(Drive.status)
        elif args.get('by_company'):
            query = db.select(
                CompanyDetails.registered_name,
                db.func.count(Drive.id)
            ).join(Drive).group_by(CompanyDetails.id).order_by(db.func.count(Drive.id).desc()).limit(5)
        else:
            query = db.select(
                Drive.job_type,
                db.func.count(Drive.id)
            ).group_by(Drive.job_type)
            
        if args.get('company_id'):
            company = f"%{args.get('company_id')}%"
            query = query.having(Drive.company_id.like(company))

        try:
            result = db.session.execute(query).all()
            if args.get('all'):
                return {'data': [("Total", result[0][0])]}
            return {'data': result}
        except Exception as e:
            print("::FETCHING DRIVE ANALYTICS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch drive analytics.")  


@analytics.route('/application')
class ApplicationAnalytics(MethodView):
    @jwt_required()
    @analytics.arguments(ApplicationsAnalyticsFilterSchema, location='query')
    @cache.cached(timeout=10, query_string=True)
    @analytics.response(HTTPStatus.OK, AnalyticsSchema)
    def get(self, args):
        query = None
        if args.get('all'):
            query = db.select(db.func.count(Application.id))
        else:
            query = db.select(
                Application.status,
                db.func.count(Application.id)
            ).group_by(Application.status)
        
        if args.get('student_id'):
            student = f"%{args.get('student_id')}%"
            query = query.where(Application.student_id.like(student))
        elif args.get('drive_id'):
            drive = f"%{args.get('drive_id')}%"
            query = query.where(Application.drive_id.like(drive))
        elif args.get('company_id'):
            company = f"%{args.get('company_id')}%"
            query = query.join(Drive).where(Drive.company_id.like(company))
        
        try:
            result = db.session.execute(query).all()
            if args.get('all'):
                return {'data': [("Total", result[0][0])]}
            return {'data': result}
        except Exception as e:
            print("::FETCHING APPLICATION ANALYTICS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch application analytics.")


@analytics.route('/placements')
class PlacementAnalytics(MethodView):
    @jwt_required()
    @analytics.arguments(PlacementAnalyticsFilterSchema, location='query')
    @cache.cached(timeout=10, query_string=True)
    @analytics.response(HTTPStatus.OK, AnalyticsSchema)
    def get(self, args):
        query = None
        if args.get('all'):
            query = db.select(db.func.count(Placement.id))
            if args.get('student_id'):
                student_id = f"%{args.get('student_id')}%"
                query = query.where(Placement.student_id.like(student_id))
            
            if args.get('company_id'):
                company_id = f"%{args.get('company_id')}%"
                query = query.where(Placement.company_id.like(company_id))
    
            if args.get('drive_id'):
                drive_id = f"%{args.get('drive_id')}%"
                query = query.where(Placement.drive_id.like(drive_id))
        else:
            query = db.select(
                CompanyDetails.registered_name,
                db.func.count(Placement.id)
            ).join(Placement).group_by(CompanyDetails.id)
        

        try:
            result = db.session.execute(query).all()
            if args.get('all'):
                return {'data': [("Total", result[0][0])]}
            return {'data': result}
        except Exception as e:
            print("::FETCHING PLACEMENT ANALYTICS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch placement analytics.")
