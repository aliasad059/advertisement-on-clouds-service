from config import rabbitmq_config
from rabbitmq_receiver import RabbitMQReceiver

if __name__ == '__main__':
    rabbitmq_receiver = RabbitMQReceiver(rabbitmq_config['AMQP_URL'])
    rabbitmq_receiver.receive_message()