import os
import requests

class ImageTaggingAPI():
    def __init__(self, config):
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']

    def get_image_tags(self, image_url, file):
        if file:
            response = requests.post(
                "https://api.imagga.com/v2/tags",
                auth=(self.api_key, self.api_secret),
                files={"image": file},
            ).json()
        else:
            response = requests.get(
                'https://api.imagga.com/v2/tags?image_url=' + image_url,
                auth=(self.api_key, self.api_secret)
            ).json()
        if response['status']['type'] == 'success':
            return response['result']['tags']
        else:
            return []
    
    def get_image_tags_with_confidence(self, image_url, mode='url'):
        if mode == 'url':
            response = self.get_image_tags(image_url=image_url, file=None)
        else:
            img_data = requests.get(image_url).content
            file_name = image_url.split('/')[-1]
            with open(file_name, 'wb') as handler:
                handler.write(img_data)
            with open(file_name, 'rb') as f:
                response = self.get_image_tags(image_url=None, file=f)
            os.remove(file_name)
        tags = {}
        for tag in response:
            tags[tag['tag']['en']] = tag['confidence']
        return tags