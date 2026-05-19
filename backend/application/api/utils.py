from http import HTTPStatus

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from application.factory import db, role_required, cache
from application.models import Role, Branch, AcademicDegree, Industry, Skill
from application.schema import RoleSchema, BranchSchema, AcademicDegreeSchema, IndustrySchema, SkillSchema


utils = Blueprint('utils', __name__, url_prefix="/api/v1/utils")

#region Roles

@utils.route('/roles')
class Roles(MethodView):
    @cache.cached(timeout=5, query_string=True)
    @utils.response(HTTPStatus.OK, RoleSchema(many=True))
    def get(self):
        try:
            return db.session.execute(db.select(Role)).scalars().all()
        except Exception as e:
            print("::FETCHING ROLES::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch roles data.")
    
    @role_required("Admin")
    @utils.arguments(RoleSchema)
    @utils.response(HTTPStatus.CREATED, RoleSchema)
    def post(self, role_data):
        try:
            db.session.add(role_data)
            db.session.commit()
            return role_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING ROLE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't create role.")

#endregion

#region Branch

@utils.route('/branch')
class Branches(MethodView):
    @cache.cached(timeout=5, query_string=True)
    @utils.response(HTTPStatus.OK, BranchSchema(many=True))
    def get(self):
        try:
            return db.session.execute(db.select(Branch)).scalars().all()
        except Exception as e:
            print("::FETCHING BRANCH::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch branch data.")
    
    @role_required("Admin")
    @utils.arguments(BranchSchema)
    @utils.response(HTTPStatus.CREATED, BranchSchema)
    def post(self, branch_data):
        try:
            db.session.add(branch_data)
            db.session.commit()
            return branch_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING BRANCH::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't create branch.")

#endregion 

#region Academic Degree

@utils.route('/academic-degree')
class AcademicDegrees(MethodView):
    @cache.cached(timeout=5, query_string=True)
    @utils.response(HTTPStatus.OK, AcademicDegreeSchema(many=True))
    def get(self):
        try:
            return db.session.execute(db.select(AcademicDegree)).scalars().all()
        except Exception as e:
            print("::FETCHING ACADEMIC DEGREES::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch academic degrees data.")

    @role_required("Admin")
    @utils.arguments(AcademicDegreeSchema)
    @utils.response(HTTPStatus.CREATED, AcademicDegreeSchema)
    def post(self, degree_data):
        try:
            db.session.add(degree_data)
            db.session.commit()
            return degree_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING ACADEMIC_DEGREE::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't create academic degree.")

#endregion 

#region Industry

@utils.route('/industry')
class Industries(MethodView):
    @cache.cached(timeout=5, query_string=True)
    @utils.response(HTTPStatus.OK, IndustrySchema(many=True))
    def get(self):
        try:
            return db.session.execute(db.select(Industry)).scalars().all()
        except Exception as e:
            print("::FETCHING INDUSTRY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch industry data.")

    @role_required("Admin")
    @utils.arguments(IndustrySchema)
    @utils.response(HTTPStatus.CREATED, IndustrySchema)
    def post(self, industry_data):
        try:
            db.session.add(industry_data)
            db.session.commit()
            return industry_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING INDUSTRY::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't create industry.")

#endregion 

#region Skills

@utils.route('/skills')
class Skills(MethodView):
    @cache.cached(timeout=5, query_string=True)
    @utils.response(HTTPStatus.OK, SkillSchema(many=True))
    def get(self):
        try:
            return db.session.execute(db.select(Skill)).scalars().all()
        except Exception as e:
            print("::FETCHING SKILLS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch skills data.")
    
    @role_required("Admin")
    @utils.arguments(SkillSchema)
    @utils.response(HTTPStatus.CREATED, SkillSchema)
    def post(self, skill_data):
        try:
            db.session.add(skill_data)
            db.session.commit()
            return skill_data
        except Exception as e:
            db.session.rollback()
            print("::CREATING SKILL::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't create skill.")

#endregion 