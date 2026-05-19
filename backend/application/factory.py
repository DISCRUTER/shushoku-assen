#region Flask Extensions

from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache


# Initializing extensions
db = SQLAlchemy()
cors = CORS(supports_credentials=True)
jwt = JWTManager()
api = Api()
cache = Cache()

#endregion

#region Authentication

# RBAC decorator
def role_required(role_name: str | list):
    from functools import wraps
    from flask import jsonify
    from flask_jwt_extended import get_jwt, jwt_required
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            required_roles = role_name if isinstance(role_name, list) else [role_name]
            if claims.get("role") in required_roles:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Access forbidden: Insufficient permissions"), 403
        return decorator
    return wrapper

#endregion