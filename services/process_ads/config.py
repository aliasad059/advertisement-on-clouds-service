import os
from dotenv import load_dotenv

load_dotenv()

UVICON_HOST = os.getenv('UVICORN_HOST')
UVICON_PORT = os.getenv('UVICORN_PORT')


psql_config = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
}

s3_config = {
    "access_key": os.getenv("S3_ACCESS_KEY"),
    "secret_key": os.getenv("S3_SECRET_KEY"),
    "bucket_name": os.getenv("S3_BUCKET_NAME"),
}

rabbitmq_config = {
    "AMQP_URL": os.getenv("RABBITMQ_AMQP_URL"),
}

image_tagging_config = {
    "api_key": os.getenv("IMAGGA_API_KEY"),
    "api_secret": os.getenv("IMAGGA_API_SECRET"),
}