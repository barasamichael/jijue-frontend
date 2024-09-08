import flask

from . import main


@main.route("/")
@main.route("/home")
@main.route("/homepage")
def index():
    return flask.render_template("main/index.html")
