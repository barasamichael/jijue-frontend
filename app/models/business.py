import flask_login
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db


class Business(flask_login.UserMixin, db.Model):
    """
    Model representing a Business.
    """

    __tablename__ = "business"

    businessId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    businessName = db.Column(db.String(200), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    dateCreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    lastUpdated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relationships
    payments = db.relationship(
        "Payment", back_populates="business", cascade="all, delete"
    )
    pushRequests = db.relationship(
        "PushRequest", back_populates="business", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return (
            f"Business(businessId={self.businessId}, businessName='"
            + f"{self.businessName}')"
        )

    @classmethod
    def registerAccount(cls, details: dict) -> "Business":
        """
        Register a new user account.

        :param details: dict - Core details of the user to be registered.
        :return: Business - The newly registered user object.
        """
        business = cls(
            businessName=details.get("businessName"),
            password=details.get("password"),
        )

        # Save user to database
        db.session.add(business)
        db.session.commit()

    def get_id(self) -> int:
        """
        Inherited UserMixin class method used to retrieve user id for
            flask_login

        :return: int - Business ID of the business.
        """
        return self.businessId

    def login(self, details=dict()) -> tuple:
        """
        Logs in the user and marks them as online.

        :param details: dict - Contains password and rebusiness_me boolean
            variable

        :return: tuple - Contains the return status and return message.
        """

        if self.verifyPassword(details.get("password", "")):
            flask_login.login_user(self, details.get("remember_me", False))

            return (1, "Login Successful")

        return (0, "Invalid password")

    def logout(self) -> tuple:
        """
        Logs out the user and updates their last seen timestamp.

        :return: tuple - Contains return status and return message.
        """
        # Logout user
        flask_login.logout_user()

        db.session.commit()

        return (1, "Logout successful")

    @property
    def password(self) -> AttributeError:
        """
        Raise an AttributeError since the password is private only
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password) -> None:
        """
        Hash the business's password
        """
        self.passwordHash = generate_password_hash(password)

    def verifyPassword(self, password: str) -> bool:
        """
        Verify the provided password with the stored hash.

        :param password: str - The password to verify.
        :return: bool - True if the password matches, False otherwise.
        """
        return check_password_hash(self.passwordHash, password)
