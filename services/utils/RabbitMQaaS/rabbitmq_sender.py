import pika

class RabbitMQSender():
    def __init__(self, AMQP_URL) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='ads')
        print("Connected to the RabbitMQ server successfully")

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key='ads', body=message)
        print(" [x] Sent %r" % message)