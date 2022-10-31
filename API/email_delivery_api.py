# DOMAIN = "sandbox793a7ecb15d54627bab7e26bde95c9ac.mailgun.org"
# API_KEY = "c5c1aeceada6e89fc4780c8997b7a88b3-8845d1b1-a96a9215"
# EMAIL_ADDRESS = "aliasad059@gmail.com"
# TEXT = "Your ad has been accepted!"
# SUBJECT = "Cloud Computing HW1"

import requests

class EmailDeliveryAPI():
    def __init__(self, domain, api_key) -> None:
        self.domain = domain
        self.api_key = api_key
    
    def send_email(self, email, subject, text):
        return requests.post(
            f"https://api.mailgun.net/v3/{self.domain}/messages",
            auth=("api", self.api_key),
            data={"from": f"<mailgun@{self.domain}>",
                "to": [email],
                "subject": subject,
                "text": text}).json()
                