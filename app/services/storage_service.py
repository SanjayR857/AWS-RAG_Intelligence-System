import boto3
from botocore.exceptions import ClientError
import os
from config import Config

class S3StorageService:

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        self.bucket_name = Config.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_path, object_name=None):
        """Upload a file to S3 bucket."""
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            print(f"File {file_path} uploaded to {self.bucket_name}/{object_name}")
            return True
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False

    def download_file(self, object_name, file_path):
        """Download a file from S3 bucket."""
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            print(f"File {object_name} downloaded from {self.bucket_name} to {file_path}")
            return True
        except ClientError as e:
            print(f"Error downloading file: {e}")
            return False
        
    def get_file(self, file_name):
        """Get a file from S3 bucket and return its content."""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)
            content = response['Body'].read()
            print(f"File {file_name} retrieved from {self.bucket_name}")
            return content
        except ClientError as e:
            print(f"Error retrieving file: {e}")
            return None