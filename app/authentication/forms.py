from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField

from wtforms.validators import EqualTo
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    businessId = IntegerField(
        "Enter your business ID",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your business ID here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    businessName = StringField(
        "Enter your business name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your business name here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={
            "autocomplete": "new-password",
        },
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")
