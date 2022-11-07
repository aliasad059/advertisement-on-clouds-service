from utils.DBaaS.psql_client import PSQLConnector
from utils.DBaaS.s3_client import S3Connector
from utils.RabbitMQaaS.rabbitmq_receiver import RabbitMQReceiver
from utils.API.image_tagging_api import ImageTaggingAPI

class ProcessAdsService:
    def __init__(self, psql_config, s3_config, rabbitmq_config, image_tagging_config) -> None:
        self.psql_client = PSQLConnector(**psql_config)
        self.s3_client = S3Connector(**s3_config)
        self.image_tagging_client = ImageTaggingAPI(**image_tagging_config)
        self.rabbitmq_client = RabbitMQReceiver(**rabbitmq_config)
        self.rabbitmq_client.receive_message()
        pass

    def process_ads(self, image_id):
        try:
            image_url = self.s3_client.get_image_url(image_id)
            image_tags = self.image_tagging_client.get_image_tags_with_confidence(image_url)
            self.psql_client.update_table('ads', 'category', image_tags[0], f'id={image_id}')
        except Exception as e:
            print(e)
            return{'status': 'failed'}
        return {'status': 'success'}
