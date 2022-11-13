import  boto3
from botocore.exceptions import ClientError


class S3Connector():
    def __init__(self, endpoint_url, access_key, secret_key, bucket_name):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

        self.bucket_name = bucket_name
        self.bucket = boto3.resource(
                's3',
                endpoint_url=endpoint_url,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            ).Bucket(bucket_name)
        
        print("Connected to the S3 server successfully")
        
    def upload_file(self, image_file, object_name):
        """
            Uploads a file to the bucket
        """
        try:
            bucket = self.bucket
            response = bucket.put_object(
                Key=object_name,
                Body=image_file,
                ACL='private'
            )
        except ClientError as e:
            print(e)
            return None
        return response
        
    def get_file_url(self, object_name):
        """
            Returns the url of the file
        """
        try:
            response = self.s3_client.generate_presigned_url(
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