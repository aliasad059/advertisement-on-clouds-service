from utils.DBaaS.psql_client import PSQLConnector
from utils.DBaaS.s3_client import S3Connector
from utils.rabbitmq_sender import RabbitMQSender

class PostAdsService:
    def __init__(self, psql_config, s3_config, rabbitmq_config) -> None:
        self.psql_client = PSQLConnector(**psql_config)
        self.s3_client = S3Connector(**s3_config)
        self.rabbitmq_client = RabbitMQSender(**rabbitmq_config)
        pass
    
    def post_ads(self, image, description, email):
        # save description and email to db
        request_id =  self.psql_client.insert_into_table("ads", "description, email, status", f"'{description}', '{email}', 'pending'")[0][0]
        request_id = str(request_id)
        # save image to s3 bucket
        s3_respose = self.s3_client.upload_file(image.file, request_id)
        print(s3_respose)

        # send message to queue
        self.rabbitmq_client.send_message(request_id)

        return {"request_id": request_id}
    

    def delete_post(self, post_id):
        try:
            self.psql_client.delete_from_table('ads', f"id = {post_ip}")
            return {"message": "Post deleted successfully"}
        except Exception as e:
            return {"error": str(e)}
        

    def get_request_status(self, post_id):
        # get request status from db
        request_status = self.psql_client.select_from_table("ads", "*", f"id = {post_id}")
        if request_status:
            if request_status[0][3] == "approved":
                return {
                    "request_id":request_status[0][0],
                    "status": request_status[0][3],
                    "category":request_status[0][4],
                    "description":request_status[0][1],
                    "image_link": request_status[0][5]
                 }
            else:
                return {
                    "request_id":request_status[0][0],
                    "status": request_status[0][3],
                    "description":request_status[0][1]
                 }
        return 'not found'