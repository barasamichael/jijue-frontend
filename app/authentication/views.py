import flask
from flask_login import current_user

from . import authentication
from .forms import LoginForm
from .forms import RegistrationForm

from ..models import Business


@authentication.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        details = {
            "businessName": form.businessName.data,
            "password": form.password.data,
        }
        Business.registerAccount(details)

        flask.flash("Registration successful. Feel free to login.", "success")
        return flask.redirect(flask.url_for("authentication.business_login"))

    return flask.render_template("authentication/register.html", form=form)


@authentication.route("/login", methods=["GET", "POST"])
def business_login():
    # Limit functionality to Anonymous Users
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("accounts.profile"))

    form = LoginForm()

    if form.validate_on_submit():
        details = {
            "password": form.password.data,
            "remember_me": form.remember_me.data,
        }

        # Find business with given email address
        business = Business.query.get(form.businessId.data)

        # Login user if found
        if business:
            success, message = business.login(details)

            if success:
                next = flask.request.args.get("next")
                if not next or not next.startswith("/"):
                    next = flask.url_for("accounts.profile")

                flask.flash(
                    f"Hello {current_user.businessName}. " + "Welcome back!"
                )
                return flask.redirect(next)

        # Notify user of invalid credentials
        flask.flash(
            "You provided invalid credentials. Please try again.", "warning"
        )

    return flask.render_template(
        "authentication/business_login.html", form=form
    )


@authentication.route("/logout")
def business_logout():
    current_user.logout()
    flask.flash("You have been logged out successfully.")
    return flask.redirect(flask.url_for("authentication.business_login"))


@authentication.route("/reauthenticate")
def reauthenticate():
    return flask.redirect(flask.url_for("authentication.business_logout"))
