import os
from dotenv import load_dotenv

load_dotenv()

UVICON_HOST = os.getenv('UVICORN_HOST')
UVICON_PORT = os.getenv('UVICORN_PORT')

image_tagging_config = {
    "api_key": os.getenv("IMAGGA_API_KEY"),
    "api_secret": os.getenv("IMAGGA_API_SECRET"),
}