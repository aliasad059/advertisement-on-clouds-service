from config import rabbitmq_config
from services.rabbitmq_receiver.rabbitmq_receiver import RabbitMQReceiver

if __name__ == '__main__':
    rabbitmq_receiver = RabbitMQReceiver(rabbitmq_config['AMQP_URL'])
    rabbitmq_receiver.receive_message()