from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField

from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    businessId = StringField(
        "Enter your business ID",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your business ID here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")
