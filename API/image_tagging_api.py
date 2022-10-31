# API_KEY = 'acc_423f6cdb27cd097'
# API_SECRET = '1047e7b03f2df466ebea2da0c92fcd1f'
# IMAGE_URL = 'https://wallpapercave.com/wp/wp3503654.jpg'

import requests

class ImageTaggingAPI():
    def __init__(self, api_key, api_secret) -> None:
        self.api_key = api_key
        self.api_secret = api_secret

    def get_image_tags(self, image_url):
        response = requests.get(
            'https://api.imagga.com/v2/tags?image_url=' + image_url,
            auth=(self.api_key, self.api_secret)
        ).json()
        return response['result']['tags']
    
    def get_image_tags_with_confidence(self, image_url):
        response = self.get_image_tags(image_url)
        tags = {}
        for tag in response:
            tags[tag['tag']['en']] = tag['confidence']
        return tags