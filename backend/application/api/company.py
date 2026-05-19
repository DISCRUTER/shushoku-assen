from http import HTTPStatus

from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, unset_access_cookies
from flask_smorest import Blueprint, abort

from application.factory import db, role_required, cache
from application.models import User, CompanyDetails, Role
from application.schema import CompanyRegisterSchema, CompanyDetailSchema, CompanyFilterSchema, CompanyUpdateSchema, ResponseSchema


company = Blueprint('company', __name__, url_prefix='/api/v1/company', description="Endpoint to retrieve info about company.")

@company.route('/')
class AllCompany(MethodView):
    @role_required(["Admin", "Student"])
    @company.arguments(CompanyFilterSchema, location='query')
    @cache.cached(timeout=5, query_string=True)
    @company.response(HTTPStatus.OK, CompanyDetailSchema(many=True))
    def get(self, args):
        query = db.select(CompanyDetails).join(CompanyDetails.user)

        if 'industry_id' in args:
            query = query.where(CompanyDetails.industry_id.in_(args.get('industry_id')))
        if 'status' in args:
            query = query.where(CompanyDetails.status == args.get('status'))
        if 'blacklisted' in args:
            query = query.where(User.blacklisted == args.get('blacklisted'))
        if args.get('name'):
            name = f"%{args.get('name')}%"
            query = query.where(CompanyDetails.registered_name.ilike(name))
        
        try:
            all_company = db.session.execute(query).scalars().all()
            return all_company
        except Exception as e:
            print("::FETCHING COMPANY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch company data.")
    
    @company.arguments(CompanyRegisterSchema)
    @company.response(HTTPStatus.CREATED, CompanyDetailSchema)
    def post(self, company_data):
        if db.session.execute(db.select(User).filter_by(email=company_data.get('email'))).scalar_one_or_none():
            abort(HTTPStatus.CONFLICT, message="Email already registered.")
        try:
            user = User(email = company_data.pop('email'))
            user.set_password(company_data.pop('password'))
            user.role = db.session.execute(db.select(Role).filter_by(name="Company")).scalar_one()

            company_details = CompanyDetails(**company_data)
            user.company_details = company_details
            
            db.session.add(user)
            db.session.commit()
            return company_details
        except Exception as e:
            db.session.rollback()
            print("::CREATING COMPANY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to register company.")

@company.route('/<string:company_id>')
class Company(MethodView):
    @jwt_required()
    @company.response(HTTPStatus.OK, CompanyDetailSchema)
    def get(self, company_id):
        try:
            company = db.session.get(CompanyDetails, company_id)
            if not company:
                abort(HTTPStatus.NOT_FOUND, message="Company not found.")
            return company
        except Exception as e:
            print("::FETCHING COMPANY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to find company.")

    @role_required(["Admin", "Company"])
    @company.arguments(CompanyUpdateSchema)
    @company.response(HTTPStatus.ACCEPTED, CompanyDetailSchema)
    def patch(self, company_update, company_id):
        try:
            company =  db.session.execute(db.select(CompanyDetails).join(CompanyDetails.user).where(CompanyDetails.id == company_id)).scalar_one_or_none()
            if not company:
                abort(HTTPStatus.NOT_FOUND, message="Company not found")
            
            role = get_jwt().get('role')

            if role == 'Company':
                if get_jwt_identity() != company.user.email:
                    abort(HTTPStatus.FORBIDDEN, message="Access denied.")
            
            if role == 'Admin':
                if 'status' in company_update:
                    company.status = company_update.pop('status')
                if 'blacklisted' in company_update:
                    company.user.blacklisted = company_update.pop('blacklisted')
            elif 'status' in company_update:
                company_update.pop('status')
            elif 'blacklisted' in company_update:
                company_update.pop('blacklisted')
                
            for key, value in company_update.items():
                setattr(company, key, value)
            
            db.session.add(company)
            db.session.commit()
            return company
        except Exception as e:
            db.session.rollback()
            print("::UPDATING COMPANY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to update company data.")

    @role_required(["Admin", "Company"])
    @company.response(HTTPStatus.NO_CONTENT, ResponseSchema)
    def delete(self, company_id):
        try:
            company = db.session.get(User, company_id)
            if not company:
                abort(HTTPStatus.NOT_FOUND, message="Company not found.")

            db.session.delete(company)
            db.session.commit()
            response = jsonify({'msg': "Access Token removed!"})
            unset_access_cookies(response=response)
            response.status_code = HTTPStatus.NO_CONTENT
            return response
        except Exception as e:
            db.session.rollback()
            print("::DELETING COMPANY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Failed to delete company data.")