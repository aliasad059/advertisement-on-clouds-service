from utils.DBaaS.psql_client import PSQLConnector
from utils.DBaaS.s3_client import S3Connector

class ProcessAdsService:
    def __init__(self, psql_config, s3_config) -> None:
        self.psql_client = PSQLConnector(**psql_config)
        self.s3_client = S3Connector(**s3_config)
        pass

    def process_ads(self, image_id):
        try:
            image_url = self.s3_client.get_image_url(image_id)
            #TODO call image tagging service
            image_tags = ['car']
            self.psql_client.update_table('ads', 'category', image_tags[0], f'id={image_id}')
        except Exception as e:
            print(e)
            return{'status': 'failed'}
        return {'status': 'success'}