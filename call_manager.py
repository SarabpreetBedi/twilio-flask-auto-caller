from twilio.rest import Client
from dotenv import load_dotenv
import os
from call_status_db import log_call_start

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
client = Client(account_sid, auth_token)

def make_call(to_number, call_id):
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="http://localhost:5000/voice",  # TwiML instructions
        status_callback=f"http://localhost:5000/status?call_id={call_id}",
        status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
        status_callback_method='POST'
    )
    log_call_start(call.sid, to_number, call_id)
    return call.sid
