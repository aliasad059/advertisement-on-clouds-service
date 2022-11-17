from utils.DBaaS.psql_client import PSQLConnector
from utils.DBaaS.s3_client import S3Connector
import requests
from config import IMAGE_TAGGING_SERVICE_URL

class ProcessAdsService:
    def __init__(self, psql_config, s3_config) -> None:
        self.psql_client = PSQLConnector(**psql_config)
        self.s3_client = S3Connector(**s3_config)
        pass

    def process_ads(self, image_id):
        response = {}
        request_row = self.psql_client.select_from_table("ads", "*", f"id = {image_id}")
        response['request_id'] = image_id
        response['email'] = request_row[0][2]
        response['description'] = request_row[0][1]
        response['request_id'] = image_id
        
        try:
            image_url = self.s3_client.get_file_url(image_id)
            tags = requests.post(IMAGE_TAGGING_SERVICE_URL, data={"image_url": image_url}).json()
            category = self.check_tags_validity(tags)
            if category:
                self.psql_client.update_table('ads', 'category', category, f'id={int(image_id)}')
                self.psql_client.update_table('ads', 'status', 'approved', f'id={int(image_id)}')
                self.psql_client.update_table('ads', 's3_url', image_url, f'id={int(image_id)}')
                response['status'] = 'approved'
                response['category'] = category
                response['image_link'] = image_url
            else:
                self.psql_client.update_table('ads', 'status', 'rejected', f'id={int(image_id)}')
                response['status'] = 'rejected'


        except Exception as e:
            print(e)
            return {'status': 'failed', 'error': str(e)}
        
        return response
        
    
    def check_tags_validity(self, tags):
        if ('vehicle' in tags) and (tags['vehicle'] > 0.5):
            category = max(tags, key=tags.get)
            return category
        return None