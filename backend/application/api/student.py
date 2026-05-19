from http import HTTPStatus

from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, unset_access_cookies
from flask_smorest import Blueprint, abort
from sqlalchemy import or_

from application.factory import db, role_required, cache
from application.models import User, StudentDetails, Role
from application.schema import StudentRegisterSchema, StudentListSchema, StudentFilterSchema, StudentUpdateSchema, ResponseSchema


students = Blueprint('students', __name__, url_prefix='/api/v1/students', description="Endpoint to access students related info.")

@students.route('/')
class AllStudents(MethodView):
    @students.doc(
        description="Returns list of students.",
        summary="Get all students."
    )
    @role_required("Admin")
    @students.arguments(StudentFilterSchema, location='query')
    @cache.cached(timeout=5, query_string=True)
    @students.response(HTTPStatus.OK, StudentListSchema(many=True))
    def get(self, args):
        query = db.select(StudentDetails).join(StudentDetails.user)

        if 'branch_id' in args:
            query = query.where(StudentDetails.branch_id.in_(args.get('branch_id')))
        if 'year' in args:
            year = args.get('year')
            query = query.where(StudentDetails.year == year)
        if 'academic_degree_id' in args:
            query = query.where(StudentDetails.academic_degree_id.in_(args.get('academic_degree_id')))
        if 'blacklisted' in args:
            query = query.where(User.blacklisted == args.get('blacklisted'))
        if args.get('name'):
            name = f"%{args.get('name')}%"
            query = query.where(or_(StudentDetails.first_name.ilike(name), StudentDetails.last_name.ilike(name)))
        
        try:
            all_students = db.session.execute(query).scalars().all()
            return all_students
        except Exception as e:
            print("::FETCHING STUDENTS::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't fetch student data.")

    @students.doc(
        description="Registers a students with all the required info.",
        summary="Register a student"
    )
    @students.arguments(StudentRegisterSchema)
    @students.response(HTTPStatus.CREATED, StudentRegisterSchema)
    def post(self, student_data):
        if db.session.execute(db.select(User).filter_by(email=student_data.get('email'))).scalar_one_or_none():
            abort(HTTPStatus.CONFLICT, message="Email already registered.")
        try:
            user = User(email=student_data.pop('email'))
            user.set_password(student_data.pop('password'))
            user.role = db.session.execute(db.select(Role).filter_by(name='Student')).scalar_one()

            student_details = StudentDetails(**student_data)
            user.student_details = student_details

            db.session.add(user)
            db.session.commit()
            return student_details
        except Exception as e:
            db.session.rollback()
            print("::CREATING STUDENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't create student.")

@students.route('/<string:student_id>')
class Student(MethodView):
    @jwt_required()
    @students.response(HTTPStatus.OK, StudentListSchema)
    def get(self, student_id):
        try:
            student = db.session.get(StudentDetails, student_id)
            if not student:
                abort(HTTPStatus.NOT_FOUND, message="Student not found.") 
            return student
        except Exception as e:
            print("::FETCHING STUDENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't find student.")
    
    @role_required(["Admin", "Student"])
    @students.arguments(StudentUpdateSchema)
    @students.response(HTTPStatus.ACCEPTED, StudentListSchema)
    def patch(self, student_update, student_id):
        try:
            student = db.session.execute(db.select(StudentDetails).join(StudentDetails.user).where(StudentDetails.id == student_id)).scalar_one_or_none()
            if not student:
                abort(HTTPStatus.NOT_FOUND, message='Student not found.')
            
            role = get_jwt().get('role')
            
            if role == 'Student':
                if get_jwt_identity() != student.user.email:
                    abort(HTTPStatus.FORBIDDEN, message="Access denied.")

            if 'blacklisted' in student_update:
                if role == 'Admin':
                    student.user.blacklisted = student_update.pop('blacklisted')
                else:
                    student_update.pop('blacklisted')

            for key, value in student_update.items():
                setattr(student, key, value)
            
            db.session.add(student)
            db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            print("::UPDATING STUDENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't update student.")
    
    @role_required(["Admin", "Student"])
    @students.response(HTTPStatus.NO_CONTENT, ResponseSchema)
    def delete(self, student_id):
        try:
            student = db.session.get(User, student_id)
            if not student:
                abort(HTTPStatus.NOT_FOUND, message="Student not found.")
            
            db.session.delete(student)
            db.session.commit()
            response = jsonify({'msg': "Access Token removed!"})
            unset_access_cookies(response=response)
            response.status_code = HTTPStatus.NO_CONTENT
            return response
        except Exception as e:
            db.session.rollback()
            print("::DELETING STUDENT::\n" + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't delete student.")
