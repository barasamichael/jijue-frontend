import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask security configuration options
    SECRET_KEY = os.environ.get("SECRET_KEY") or "uz%1+3T}%LzG)7ORH5q;&~HoTeL&"

    # SQLAlchemy configuration options
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME = 0.5

    # Application configuration options
    ORGANIZATION_NAME = os.environ.get("ORGANIZATION_NAME") or "Jijue"
    BACKEND_URL = os.environ.get("BACKEND_URL") or "http://localhost:3000"

    # File upload configuration options
    UPLOAD_FOLDER = os.path.join(basedir + "/app/static/documents/")

    # M-pesa Payment Settings
    CONSUMER_KEY = os.environ.get(
        "CONSUMER_KEY", "E7RkuNKKVFG3p2nWjEM78RcbFOwH2qb5UHpGvpOhzodFGbHV"
    )
    CONSUMER_SECRET = os.environ.get(
        "CONSUMER_SECRET",
        "tQw44mUODFBqUk25oS5NweJBMrlvdWwkYdap6P3895kekW2LmLFcHT4Lvjr4figm",
    )

    BASE_URL = "https://sandbox.safaricom.co.ke"
    ACCESS_TOKEN_URL = "oauth/v1/generate?grant_type=client_credentials"
    STK_PUSH_URL = "mpesa/stkpush/v1/processrequest"
    STK_QUERY_URL = "mpesa/stkpushquery/v1/query"
    CALLBACK_URL = "https://jisortublow.co.ke/client/payment/stk-callback"
    MPESA_LOG_FILE = "M_Pesa_stk_response.json"

    BUSINESS_SHORT_CODE = os.environ.get("BUSINESS_SHORT_CODE", "174379")
    TILL_NUMBER = os.environ.get("TILL_NUMBER", "8976288")
    PASSKEY = os.environ.get(
        "PASSKEY",
        "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
    )

    # Fetch Callbacks Settings
    API_SERVER_INDEX = (
        os.environ.get("API_SERVER_INDEX") or "http://127.0.0.1:5000/"
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVELOPMENT_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "development.db")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("TEST_DATABASE_URL") or "sqlite:///:memory"
    )
    SECRET_KEY = "chdbvbjncgyvgtbhhtjhmkldfhgcavbxntkuymluv"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    SESSION_COOKIE_SECURE = True

    DB_NAME = os.environ.get("DB_NAME") or "jijue"
    DB_USERNAME = os.environ.get("DB_USERNAME") or "root"
    DB_HOST = os.environ.get("DB_HOST") or "localhost"
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or "MySQLXXX-123a8910"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PRODUCTION_DATABASE_URL")
        or f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}"
        + f"/{DB_NAME}"
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # TODO: Email errors to the administrators


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
