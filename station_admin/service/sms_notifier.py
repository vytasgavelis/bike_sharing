import os
from twilio.rest import Client

class SmsNotifier:

    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)

    def notify_user(self, number: str) -> None:
        message = self.client.messages \
            .create(
            body="Your session is near it's end time.",
            from_='+19794935778',
            to=number
        )
