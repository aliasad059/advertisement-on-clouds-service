import pika

class RabbitMQConnector():
    def __init__(self, AMQP_URL) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='ads')
        print("Connected to the RabbitMQ server successfully")

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key='ads', body=message)
        print(" [x] Sent %r" % message)

    def receive_message(self):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
        self.channel.basic_consume(queue='ads', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()