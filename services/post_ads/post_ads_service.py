class PostAdsService:
    def __init__(self)->None:
        pass
    
    def post_ads(self, image, description, email):
        # save description and email to db
        # save image to s3 bucket
        # send message to queue
        # return request_id
        pass

    def get_request_status(self, post_id):
        # get request status from db
        # return request status
        pass
