import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
account_sid = 'ACccbc8ef9a96381ebb8bf39ec928faa47'
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
auth_token = '01a4a2b9ce134791d1dc1b8740a22284'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+19794935778',
                     to='+37062815944'
                 )

print(message.sid)