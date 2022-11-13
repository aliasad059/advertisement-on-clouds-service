import pika, sys, os
import requests
from config import PROCESS_ADS_SERVICE_URL

class RabbitMQReceiver():
    def __init__(self, AMQP_URL) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='ads')
        print("Connected to the RabbitMQ server successfully")

    def receive_message(self):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body.decode())
            requests.post(PROCESS_ADS_SERVICE_URL, data={"image_id": body.decode()})
            
        try:
            self.channel.basic_consume(queue='ads', on_message_callback=callback, auto_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.close_connection()
            sys.exit(0)

    def close_connection(self):
        self.connection.close()