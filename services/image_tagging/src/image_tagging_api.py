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