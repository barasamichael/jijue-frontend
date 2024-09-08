from flask import Blueprint
from flask import current_app

accounts = Blueprint("accounts", __name__)
from . import views, errors


@accounts.app_context_processor
def global_variables():
    """
    Provide global variables for templates within the 'accounts' blueprint.

    :return: A dictionary containing global variables to inject into templates.
    :rtype: dict

    :params: None
    """
    return dict(
        app_name=current_app.config["ORGANIZATION_NAME"],
        api_server=current_app.config["API_SERVER_INDEX"]
    )
