import flask
import flask_login
import flask_moment
import flask_mailman
import flask_sqlalchemy

from config import config

# set endpoint for the login page
login_manager = flask_login.LoginManager()
login_manager.login_view = "authentication.business_login"
login_manager.refresh_view = "authentication.reauthenticate"
login_manager.needs_refresh_message = (
    "To protect your account, please login afresh to access this page."
)
login_manager.needs_refresh_message_category = "info"


@login_manager.user_loader
def load_user(business_id):
    from .models import Business

    return Business.query.get(int(business_id))


db = flask_sqlalchemy.SQLAlchemy()
mail = flask_mailman.Mail()
moment = flask_moment.Moment()


def create_app(config_name="default"):
    """
    Initialize and configure the Flask application.

    :param config_name: str - The name of the configuration class defined in
        config.py.

    :return app: Flask - The configured Flask application instance.
    """
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # Enable SSL redirection if configured
    if app.config["SSL_REDIRECT"]:
        from flask_sslify import SSLify

        SSLify(app)

    # Register blueprints for different parts of the application
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .accounts import accounts as accounts_blueprint

    app.register_blueprint(accounts_blueprint, url_prefix="/account")

    from .authentication import authentication as authentication_blueprint

    app.register_blueprint(
        authentication_blueprint, url_prefix="/authentication"
    )

    return app
