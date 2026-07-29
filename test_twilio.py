from twilio.rest import Client
from config import Config

client = Client(
    Config.TWILIO_ACCOUNT_SID,
    Config.TWILIO_AUTH_TOKEN
)

message = client.messages.create(
    body="MJCA Twilio test message!",
    from_=Config.TWILIO_PHONE_NUMBER,
    to="+16156060800"
)

print(message.sid)