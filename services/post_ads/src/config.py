import os
from dotenv import load_dotenv

load_dotenv()

UVICORN_HOST = os.getenv('UVICORN_HOST')
UVICORN_PORT = os.getenv('UVICORN_PORT')


psql_config = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "database": os.getenv("POSTGRES_DB"),
}

s3_config = {
    "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
    "access_key": os.getenv("S3_ACCESS_KEY"),
    "secret_key": os.getenv("S3_SECRET_KEY"),
    "bucket_name": os.getenv("S3_BUCKET_NAME"),
}

rabbitmq_config = {
    "AMQP_URL": os.getenv("RABBITMQ_AMQP_URL"),
}

EMAIL_DELIVERY_SERVICE_URL=os.getenv("EMAIL_DELIVERY_SERVICE_URL")
EMAIL_SUCCESS_SUBJECT='Request received'
EMAIL_SUCCESS_TEXT="Your request has been received and is being processed.\n" + \
                    "You will be notified when it is approved.\n\n"+ \
                    "Your request id is: \n\t REQUEST_ID\n\n\n"+ \
                    "Best regards,\n" + \
                    "Your friends at the Ads On Cloud Service"