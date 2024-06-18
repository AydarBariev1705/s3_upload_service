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

# def main():
#     s3_client = S3Client(
#         access_key="7d12f2af5296405f9417d36169d11bc1",
#         secret_key="18afe22c3f2049229a45dc49175983a1",
#         endpoint_url="https://s3.storage.selcloud.ru",
#         bucket_name="barievbucket1",
#     )
#     s3_client.upload_file("3333.jpg")
#
#
# main()
