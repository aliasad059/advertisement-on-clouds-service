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
        
    def upload_file(self, image_file: bytes, object_name: str) -> dict:
        """
        Uploads the given image file to an S3 bucket under the specified object name.

        Args:
            image_file (bytes): The file to upload, in bytes.
            object_name (str): The name of the object to create in the bucket.

        Returns:
            dict: S3 response object if the upload succeeded.
            None: If an exception occurred, None is returned.

        Raises:
            ClientError: If an error occurs when attempting to upload to S3.
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
        
    def get_file_url(self, object_name: str) -> str:
        """
        Generates a presigned URL for the given S3 object.

        Args:
            object_name (str): The name of the object for which to create the presigned URL.

        Returns:
            str: A presigned URL allowing access to the object if successful.
            None: If an exception occurred, None is returned.

        Raises:
            ClientError: If an error occurs when attempting to generate the presigned URL.
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
    
    def delete_file(self, object_name: str) -> dict:
        """
        Deletes the specified file from the S3 bucket.

        Args:
            object_name (str): The name of the object to delete.

        Returns:
            dict: S3 delete operation response object if the delete succeeded.
            None: If an exception occurred, None is returned.

        Raises:
            ClientError: If an error occurs when attempting to delete from S3.
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