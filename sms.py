#Twilioi helper functions
from twilio.rest import Client
from flask import current_app

def send_sms(phone_number, message):
    client = Client(
        current_app.config["TWILIO_ACCOUNT_SID"],
        current_app.config["TWILIO_AUTH_TOKEN"],
    )
    client.messages.create(
        body=message,
        from_=current_app.config["TWILIO_PHONE_NUMBER"],
        to=phone_number,
    )