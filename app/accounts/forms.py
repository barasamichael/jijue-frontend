from flask_wtf import FlaskForm
from wtforms import TimeField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import IntegerField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import DateTimeField
from wtforms.validators import URL
from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import EqualTo
from wtforms.validators import Optional
from wtforms.validators import DataRequired


class MemberForm(FlaskForm):
    fullName = StringField(
        "Full Name", validators=[DataRequired(), Length(max=200)]
    )
    emailAddress = StringField(
        "Email Address", validators=[DataRequired(), Email(), Length(max=100)]
    )
    phoneNumber = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Regexp(r"^\+?1?\d{9,14}$", message="Invalid phone number format."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo("confirmPassword", message="Passwords must match."),
        ],
    )
    confirmPassword = PasswordField(
        "Confirm Password", validators=[DataRequired()]
    )
    dorm = StringField("Dorm", validators=[Optional(), Length(max=4)])
    house = StringField("House", validators=[DataRequired(), Length(max=50)])
    yearOfGraduation = StringField(
        "Year of Graduation",
        validators=[
            Optional(),
            Regexp(r"^\d{4}$", message="Invalid year format."),
        ],
    )
    bio = TextAreaField("Bio", validators=[Optional()])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    country = StringField("Country", validators=[Optional(), Length(max=255)])
    currentPosition = StringField(
        "Current Position", validators=[Optional(), Length(max=255)]
    )
    institution = StringField(
        "Institution", validators=[Optional(), Length(max=255)]
    )
    role = SelectField(
        "Role",
        choices=[("member", "Member"), ("administrator", "Administrator")],
        default="member",
    )
    isActive = BooleanField("Is Active", default=True)
    submit = SubmitField("Save Member")


class ApplicationForm(FlaskForm):
    coverLetter = TextAreaField("Cover Letter", validators=[Optional()])
    submit = SubmitField("Apply")


class BusinessForm(FlaskForm):
    name = StringField(
        "Business Name", validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField("Description", validators=[Optional()])
    contactEmail = StringField(
        "Contact Email", validators=[DataRequired(), Email(), Length(max=120)]
    )
    phoneNumber = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Regexp(r"^\+?1?\d{9,14}$", message="Invalid phone number format."),
        ],
    )
    location = StringField(
        "Location", validators=[DataRequired(), Length(max=255)]
    )
    openingHours = TimeField("Opening Hours", validators=[DataRequired()])
    closingHours = TimeField("Closing Hours", validators=[DataRequired()])
    services = TextAreaField("Services", validators=[Optional()])
    website = StringField("Website", validators=[Optional(), URL()])
    submit = SubmitField("Save Business")


class OpportunityForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    institution = StringField(
        "Institution", validators=[DataRequired(), Length(max=255)]
    )
    position = StringField(
        "Position", validators=[DataRequired(), Length(max=255)]
    )
    workingMethod = SelectField(
        "Working Method",
        choices=[
            ("onsite", "Onsite"),
            ("offsite", "Offsite"),
            ("hybrid", "Hybrid"),
        ],
        default="onsite",
        validators=[DataRequired()],
    )
    description = TextAreaField("Description", validators=[Optional()])
    category = SelectField(
        "Category", validators=[Optional(), Length(max=120)]
    )
    location = StringField(
        "Location", validators=[Optional(), Length(max=120)]
    )
    deadline = DateTimeField("Deadline", validators=[Optional()])
    posterId = IntegerField("Poster ID", validators=[Optional()])
    submit = SubmitField("Save Opportunity")


class PlacementRequestForm(FlaskForm):
    course = StringField(
        "Course", validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField(
        "Description", validators=[Optional(), Length(max=255)]
    )
    deadline = DateTimeField("Deadline", validators=[Optional()])
    memberId = IntegerField("Member ID", validators=[DataRequired()])
    submit = SubmitField("Save Placement Request")


class MemberSkillForm(FlaskForm):
    skillId = SelectField("Skill ID", validators=[DataRequired()])
    submit = SubmitField("Save Skill")
