import os

import flask
import requests
from flask import jsonify
from flask_login import current_user
from flask_login import login_required
from werkzeug.utils import secure_filename

from . import accounts

from .. import db
from ..models import Business
from ..models import Payment
from ..models import PushRequest

from utilities.mpesa_payment import get_access_token
from utilities.mpesa_payment import initiate_stk_push
from utilities.mpesa_payment import query_stk_status


@accounts.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if flask.request.method == "POST":
        # Check if the user uploaded all required files
        if (
            "nationalID" not in flask.request.files
            or "businessCertificate" not in flask.request.files
            or "kraPin" not in flask.request.files
        ):
            flask.flash("Please upload all required documents.", "danger")
            return flask.redirect(flask.url_for("accounts.profile"))

        national_id_file = flask.request.files["nationalID"]
        business_cert_file = flask.request.files["businessCertificate"]
        kra_pin_file = flask.request.files["kraPin"]

        folder = os.path.join(
            flask.current_app.config["UPLOAD_FOLDER"],
            str(current_user.businessId),
        )

        # Ensure the upload folder exists
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        # Save files to the upload folder
        national_id_path = os.path.join(
            folder,
            secure_filename("national_id"),
        )
        business_cert_path = os.path.join(
            folder,
            secure_filename("business_certificate"),
        )
        kra_pin_path = os.path.join(
            folder,
            secure_filename("kra_pin"),
        )

        national_id_file.save(national_id_path)
        business_cert_file.save(business_cert_path)
        kra_pin_file.save(kra_pin_path)

        # Redirect to the payment page
        flask.flash("Make payment to cover verification costs", "warning")
        return flask.redirect(flask.url_for("accounts.payments"))
    return flask.render_template("accounts/profile.html")


@accounts.route("/documents/verification", methods=["GET"])
@login_required
def perform_verification():
    # Create documents folder path
    folder = os.path.join(
        flask.current_app.config["UPLOAD_FOLDER"], str(current_user.businessId)
    )

    # Prepare files and data for the backend request
    files = {
        "nationalID": open(os.path.join(folder, "national_id"), "rb"),
        "businessCertificate": open(
            os.path.join(folder, "business_certificate"), "rb"
        ),
        "kraPin": open(os.path.join(folder, "kra_pin"), "rb"),
    }
    data = {
        "businessId": current_user.businessId,
        "businessName": current_user.businessName,
    }

    try:
        backend_url = flask.current_app.config["BACKEND_URL"]
        response = requests.post(
            f"{backend_url}/register", files=files, data=data
        )
        response_data = response.json()

        if response.status_code == 200:
            flask.flash("Registration and verification successful.", "success")
            return flask.render_template(
                "result.html", result=response_data["credential"]
            )
        else:
            flask.flash(
                response_data.get("message", "Verification failed."),
                "danger",
            )
            return flask.redirect(flask.url_for("index"))

    except requests.exceptions.RequestException as e:
        flask.flash(f"Error connecting to backend: {e}", "danger")
        return flask.redirect(flask.url_for("index"))


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
