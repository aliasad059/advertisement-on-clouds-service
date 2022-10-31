import  boto3


class S3Connector():
    def __init__(self, access_key, secret_key, bucket_name):
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.bucket = self.s3.Bucket(bucket_name)
        print("Connected to the S3 server successfully")
        
    def upload_file(self, file_name, object_name=None):
        """
            Uploads a file to the bucket
        """
        if object_name is None:
            object_name = file_name
        try: 
            response = self.bucket.upload_file(file_name, object_name)
            print("Uploaded file successfully")
            return response

        except Exception as e:
            print("Error uploading file: ", e)
            return None
    
    def download_file(self, object_name, file_name):
        """
            Downloads a file from the bucket
        """
        try:
            self.bucket.download_file(object_name, file_name)
            print("Downloaded file successfully")
        except Exception as e:
            print("Error downloading file: ", e)
    
    def delete_file(self, object_name):
        """
            Deletes a file from the bucket
        """
        try:
            self.bucket.Object(object_name).delete()
            print("Deleted file successfully")
        except Exception as e:
            print("Error deleting file: ", e)
    
    def list_files(self):
        """
            Lists all the files in the bucket
        """
        try:
            for object in self.bucket.objects.all():
                print(object.key)
        except Exception as e:
            print("Error listing files: ", e)
        