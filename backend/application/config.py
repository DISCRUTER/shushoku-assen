from datetime import timedelta


class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    # Api Configuration
    API_TITLE = "Placement Portal"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SERVER_NAME = "localhost:3000"

    # Sql-Alchemy Configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    # JWT Configuration
    JWT_SECRET_KEY = "Very-secret-key-I-will-tell-no-one-about-ever-ever-ever"
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_COOKIE_SECURE = False
    JWT_SESSION_COOKIE = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    JWT_COOKIE_CSRF_PROTECT = True

    # Caching Configuration
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300