import flask

from flask import jsonify
from flask_login import login_required

from . import accounts

from .. import db
from ..models import Business
from ..models import Payment
from ..models import PushRequest

from utilities.mpesa_payment import get_access_token
from utilities.mpesa_payment import initiate_stk_push
from utilities.mpesa_payment import query_stk_status


@accounts.route("/profile")
@login_required
def profile():
    return flask.render_template("accounts/profile.html")


@accounts.route("/payments")
@login_required
def payments():
    return flask.render_template("accounts/payments.html")


@accounts.route("/payment/stk-push", methods=["GET", "POST"])
@login_required
def payment_stk_push():
    data = flask.request.json

    # Confirm all required values are present
    required_fields = ["phoneNumber", "amount", "businessId"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"})

    # Extract passed JSON values
    phone_number = data.get("phoneNumber")
    amount = data.get("amount")
    business_id = data.get("businessId")

    # Ensure that the business actually exists
    if not Business.query.get(business_id):
        return jsonify(
            {"error": "Business does not exist. Contact our Help Center"}
        )

    # Get authentication token
    response = get_access_token()
    access_token = response.get_json().get("access_token")

    # Initiate STK/IN push request
    response = initiate_stk_push(
        access_token=access_token, phone_number=phone_number, amount=amount
    )

    # Check for failed STK/IN push request
    if response.get("errorMessage"):
        return jsonify({"code": None, "error": response.get("errorMessage")})

    # Save record in database
    details = {
        "businessId": business_id,
        "checkoutRequestId": response.get("CheckoutRequestID"),
    }
    PushRequest.create(details)

    # Return response
    return jsonify(
        {
            "code": response.get("ResponseCode"),
            "message": response.get("CustomerMessage"),
            "checkoutRequestId": response.get("CheckoutRequestID"),
        }
    )


@accounts.route("/payment/stk-query", methods=["POST"])
def payment_stk_query():
    # Get JSON values passed
    checkout_request_id = flask.request.json.get("checkoutRequestId")

    # Get authentication token
    response = get_access_token()
    access_token = response.get_json().get("access_token")

    # Send STK/IN query request
    response = query_stk_status(
        access_token=access_token, checkout_request_id=checkout_request_id
    )

    if not isinstance(response, dict):
        response = response.get_json()

    # Check for any errors in the response
    if response.get("errorMessage"):
        return jsonify(
            {
                "code": None,
                "error": response.get("errorMessage") + ". Check your phone.",
            }
        )

    # Return response
    return jsonify(
        {
            "code": response.get("ResultCode"),
            "message": response.get("ResultDesc"),
        }
    )


@accounts.route("/payment/stk-callback", methods=["POST"])
def payment_stk_callback():
    response = flask.request.get_json()
    response = response["Body"]["stkCallback"]

    result_code = response["ResultCode"]
    if result_code == 0:
        payment_details = response["CallbackMetadata"]["Item"]

        # Get associated business Id
        record = PushRequest.query.filter_by(
            checkoutRequestId=response["CheckoutRequestID"]
        ).first()
        if not record:
            return jsonify({"error": "Ooops something went wrong"})

        # Save payment details
        amount = next(
            (
                item["Value"]
                for item in payment_details
                if item["Name"] == "Amount"
            ),
            None,
        )
        details = {
            "amount": int(amount),
            "receiptNumber": next(
                (
                    item["Value"]
                    for item in payment_details
                    if item["Name"] == "MpesaReceiptNumber"
                ),
                None,
            ),
            "paymentDate": next(
                (
                    item["Value"]
                    for item in payment_details
                    if item["Name"] == "PaymentDate"
                ),
                None,
            ),
            "phoneNumber": next(
                (
                    item["Value"]
                    for item in payment_details
                    if item["Name"] == "PhoneNumber"
                ),
                None,
            ),
            "paymentMethod": "M-PESA",
            "businessId": record.businessId,
        }

        Payment.create(details)

        # Delete the temporary PushRequest record
        db.session.delete(record)
        db.session.commit()

    return jsonify({"message": "Payment details well recieved"})
