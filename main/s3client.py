from botocore.session import get_session
from botocore.exceptions import ClientError


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    def get_client(self):
        client = self.session.create_client('s3', **self.config)
        return client

    def upload_file(
            self,
            file, object_name
    ):

        try:
            client = self.get_client()
            client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file,
            )

            print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")


