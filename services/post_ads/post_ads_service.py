from utils.DBaaS.psql_client import PSQLConnector
from utils.DBaaS.s3_client import S3Connector
from utils.RabbitMQaaS.rabbitmq_client import RabbitMQConnector

class PostAdsService:
    def __init__(self, psql_config, s3_config, rabbitmq_config) -> None:
        self.psql_client = PSQLConnector(**psql_config)
        self.s3_client = S3Connector(**s3_config)
        self.rabbitmq_client = RabbitMQConnector(**rabbitmq_config)
        pass
    
    def post_ads(self, image, description, email):
        # save description and email to db
        request_id =  self.psql_client.insert_into_table("ads", description, email)

        # save image to s3 bucket
        s3_respose = self.s3_client.upload_file(image, request_id)
        print(s3_respose)

        # send message to queue
        self.rabbitmq_client.send_message(request_id)

        return request_id

    def get_request_status(self, post_id):
        # get request status from db
        request_status = self.psql_client.select_from_table("ads", "state", f"id = {post_id}")
        return request_status
