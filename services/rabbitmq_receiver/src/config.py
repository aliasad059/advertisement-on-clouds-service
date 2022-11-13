import os
from dotenv import load_dotenv

load_dotenv()

rabbitmq_config = {
    "AMQP_URL": os.getenv("RABBITMQ_AMQP_URL"),
}

PROCESS_ADS_SERVICE_URL = os.getenv("PROCESS_ADS_SERVICE_URL")