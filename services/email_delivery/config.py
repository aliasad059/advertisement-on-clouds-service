import os
from dotenv import load_dotenv

load_dotenv()

UVICON_HOST = os.getenv('UVICORN_HOST')
UVICON_PORT = os.getenv('UVICORN_PORT')

email_delivery_config = {
    "domain": os.getenv("EMAIL_DELIVERY_DOMAIN"),
    "api_key": os.getenv("EMAIL_DELIVERY_API_KEY")
}