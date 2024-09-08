import os
import base64
import logging
import requests
from datetime import datetime


import flask
from flask import jsonify


def getConfig(app):
    with app.app_context():
        return app.config


def get_access_token():
    """Retrieves the access token"""
    config = getConfig(flask.current_app._get_current_object())
    access_token_url = os.path.join(
        config["BASE_URL"], config["ACCESS_TOKEN_URL"]
    )

    headers = {
        "Content-Type": "application/json",
    }
    auth = (config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        result = response.json()
        access_token = result["access_token"]
        return jsonify({"access_token": access_token})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})


def initiate_stk_push(
    access_token=None, amount=1, phone_number="254463744444"
):
    """Initiates an STK push"""
    config = getConfig(flask.current_app._get_current_object())

    if not access_token:
        return jsonify({"error": "Access token not provided"})

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        (
            config["BUSINESS_SHORT_CODE"] + config["PASSKEY"] + timestamp
        ).encode()
    ).decode()
    query_url = os.path.join(config["BASE_URL"], config["STK_PUSH_URL"])
    stk_push_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    stk_push_payload = {
        "BusinessShortCode": config["BUSINESS_SHORT_CODE"],
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": config["TILL_NUMBER"],
        "PhoneNumber": phone_number,
        "CallBackURL": config["CALLBACK_URL"],
        "AccountReference": "DaSKF Raffle",
        "TransactionDesc": "STK/IN Push",
    }

    try:
        response = requests.post(
            query_url, headers=stk_push_headers, json=stk_push_payload
        )

        return response.json()

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})


def query_stk_status(access_token=None, checkout_request_id=None):
    """Queries the STK/IN push status"""
    config = getConfig(flask.current_app._get_current_object())

    if not access_token:
        logging.error("Access token not provided")
        return jsonify({"error": "Transaction failed. Try again later."})

    if not checkout_request_id:
        logging.error("Checkout Request ID not provided")
        return jsonify({"error": "Transaction failed. Try again later."})

    query_url = os.path.join(config["BASE_URL"], config["STK_QUERY_URL"])
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        (
            config["BUSINESS_SHORT_CODE"] + config["PASSKEY"] + timestamp
        ).encode()
    ).decode()

    query_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    query_payload = {
        "BusinessShortCode": config["BUSINESS_SHORT_CODE"],
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id,
    }

    try:
        response = requests.post(
            query_url, headers=query_headers, json=query_payload
        )
        return response.json()

    except Exception as e:
        return {"errorMessage": str(e)}
