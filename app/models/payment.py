from app import db


class Payment(db.Model):
    """
    Model representing a Payment.
    """

    __tablename__ = "payment"

    paymentId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paymentMethod = db.Column(db.String(30))
    receiptNumber = db.Column(db.String(30), nullable=False)
    paymentDate = db.Column(db.String(16))
    dateCreated = db.Column(db.DateTime, default=db.func.current_timestamp())
    lastUpdated = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    businessId = db.Column(
        db.Integer, db.ForeignKey("business.businessId", ondelete="SET NULL")
    )

    # Relationships
    business = db.relationship("Business", back_populates="payments")

    def __repr__(self) -> str:
        return f"Payment(paymentId={self.paymentId}, amount={self.amount})"

    @classmethod
    def create(cls, details: dict) -> "Payment":
        """
        Create a new Payment record.

        :param details: dict - Details required to create the payment record.
        :return: Payment - The created Payment instance.
        """
        payment = cls(
            amount=details.get("amount"),
            paymentMethod=details.get("paymentMethod"),
            receiptNumber=details.get("receiptNumber"),
            paymentDate=details.get("paymentDate"),
            businessId=details.get("businessId"),
        )
        db.session.add(payment)
        db.session.commit()
        return payment

    def getDetails(self) -> dict:
        """
        Get the details of the Payment record.

        :return: dict - Details of the Payment, suitable for JSON
            serialization.
        """
        return {
            "paymentId": self.paymentId,
            "amount": self.amount,
            "paymentMethod": self.paymentMethod,
            "receiptNumber": self.receiptNumber,
            "paymentDate": self.paymentDate,
            "businessId": self.businessId,
            "dateCreated": self.dateCreated.isoformat(),
            "lastUpdated": self.lastUpdated.isoformat(),
        }
