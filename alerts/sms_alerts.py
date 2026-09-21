from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_PHONE_NUMBER = "+17372508034"
TO_PHONE_NUMBER = "+916235411730"


def send_sms():
    """Send the Twilio trial SMS alert."""

    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )

    message = client.messages.create(
        body="sms_internal_alerts",
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )

    print("SMS alert sent successfully.")
    print("Message SID:", message.sid)
    print("Status:", message.status)