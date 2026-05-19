from http import HTTPStatus

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies, jwt_required, get_jwt_identity

from application.factory import db
from application.models import User
from application.schema import UserLoginSchema, UserLoginResponseSchema, ResponseSchema
from application.util_enum import CompanyStatus


# Registering blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth/v1', description="User authentication")


# Login class implementation
@auth.route('/login')
class Login(MethodView):

    @auth.doc(
        description="Login endpoint for users.",
        summary="Login endpoint."
    )
    @auth.arguments(UserLoginSchema)
    @auth.response(HTTPStatus.OK, UserLoginResponseSchema)
    def post(self, login_data):
        try:
            user = db.session.execute(db.select(User).filter_by(email=login_data.get('email'))).scalar_one_or_none()
        except Exception as e:
            print(":LOGGING IN USER:: " + str(e))
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Couldn't login at the moment.")

        if user and user.check_password(login_data.get('password')):
            if user.blacklisted:
                abort(HTTPStatus.FORBIDDEN, message="Your account has been blacklisted.")
            
            if user.role.name == 'Company':
                if user.company_details.status != CompanyStatus.APPROVED:
                    abort(HTTPStatus.FORBIDDEN, message="Your account is not approved by Admin yet.")

            claims = {
                'role': user.role.name
            }
            access_token = create_access_token(identity=user.email, additional_claims=claims)
            payload = {
                'id': user.id,
                'role': user.role.name
            }
            response = jsonify(payload)
            response.status_code = HTTPStatus.OK

            set_access_cookies(response=response, encoded_access_token=access_token)

            return response
        else:
            abort(HTTPStatus.BAD_REQUEST, message="Invalid credentials.")



# Logout class implementation
@auth.route('/logout')
class Logout(MethodView):

    @auth.doc(
        description="Logout endpoint for users.",
        summary="Logout endpoint."
    )
    @jwt_required()
    @auth.response(HTTPStatus.OK, ResponseSchema)
    def post(self):
        identity = get_jwt_identity()
        user = db.session.execute(db.select(User).filter_by(email=identity)).scalar_one_or_none()
        if user:
            response = jsonify({'msg': "Access Token removed!"})
            unset_access_cookies(response=response)
            response.status_code = HTTPStatus.OK
            return response
        else:
            abort(HTTPStatus.BAD_REQUEST, message="Invalid logout attempt.")
