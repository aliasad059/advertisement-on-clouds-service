import os
from dotenv import load_dotenv

load_dotenv()

rabbitmq_config = {
    "AMQP_URL": os.getenv("RABBITMQ_AMQP_URL"),
}