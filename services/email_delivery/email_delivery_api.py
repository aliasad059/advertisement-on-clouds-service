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
                