from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

def send_sms(to_number, animal_name, confidence, time):  #Sends SMS alert
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        print("Twilio credentials are not set properly.")
        return
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message_body = (
        f"🚨 ALERT!\n"
        f"Wild Animal Detected: {animal_name}\n"
        f"Confidence: {confidence:.2f}\n"
        f"Time: {time}\n"
        f"Please take immediate action."
    )

    client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=to_number
    )

    print("SMS alert sent successfully.")

