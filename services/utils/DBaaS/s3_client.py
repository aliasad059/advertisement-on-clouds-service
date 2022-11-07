import  boto3
from botocore.exceptions import ClientError


class S3Connector():
    def __init__(self, endpoint_url, access_key, secret_key, bucket_name):
        self.s3 = boto3.client(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            ) 
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name).create()
        print("Connected to the S3 server successfully")
        
    def upload_file(self, file_path, object_name):
        """
            Uploads a file to the bucket
        """
        try:
            bucket = self.bucket
            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
        except ClientError as e:
            print(e)
            return False
        return True
        
    def get_file_url(self, object_name):
        """
            Returns the url of the file
        """
        try:
            response = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=3600
            )
        except ClientError as e:
            print(e)
            return None
        return response
    
    def delete_file(self, object_name):
        """
            Deletes a file from the bucket
        """
        try:
            object = self.bucket.Object(object_name)
            response = object.delete(
                VersionId='string',
            )
        except ClientError as e:
            print(e)
            return None
        return response