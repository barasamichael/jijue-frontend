from app import db


class PushRequest(db.Model):
    """
    Model representing a Push Request.
    """

    __tablename__ = "pushrequest"

    pushRequestId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    checkoutRequestId = db.Column(db.String(100), nullable=False)
    businessId = db.Column(
        db.Integer, db.ForeignKey("business.businessId", ondelete="SET NULL")
    )
    dateCreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    lastUpdated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Reason can vary from monthly subscription to donation to event payment
    reason = db.Column(db.String(30), default="Monthly Subscription")

    # Relationships
    business = db.relationship("Business", back_populates="pushRequests")

    def __repr__(self) -> str:
        return f"PushRequest(pushRequestId={self.pushRequestId})"

    @classmethod
    def create(cls, details: dict) -> "PushRequest":
        """
        Create a new Push Request.

        :param details: dict - Details required to create the push request
            record.

        :return: PushRequest - The created PushRequest instance.
        """
        push_request = cls(
            checkoutRequestId=details.get("checkoutRequestId"),
            businessId=details.get("businessId"),
            reason=details.get("reason"),
        )
        db.session.add(push_request)
        db.session.commit()
        return push_request

    def getDetails(self) -> dict:
        """
        Get the details of the Push Request in a JSON serializable format.

        :return: dict - Details of the Push Request.
        """
        return {
            "pushRequestId": self.pushRequestId,
            "checkoutRequestId": self.checkoutRequestId,
            "businessId": self.businessId,
            "dateCreated": self.dateCreated.isoformat(),
            "lastUpdated": self.lastUpdated.isoformat(),
        }

    def delete(self) -> None:
        """
        Delete the Push Request from the database.

        :return: None
        """
        db.session.delete(self)
        db.session.commit()
