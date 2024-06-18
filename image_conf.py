from io import BytesIO

from PIL import Image
from s3client import S3Client
from config import ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, BUCKET_NAME


def make_resize(image_data, filename, sizes=None, ):
    s3_client = S3Client(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        endpoint_url=ENDPOINT_URL,
        bucket_name=BUCKET_NAME,
    )
    if sizes:
        img = Image.open(BytesIO(image_data))
        resized_image = img.resize(sizes)
        img_byte_arr = BytesIO()
        resized_image.save(img_byte_arr, format=img.format)
        img_byte_arr = img_byte_arr.getvalue()
        s3_client.upload_file(img_byte_arr, filename)

    else:
        s3_client.upload_file(image_data, filename)

# def main(filename: str):
#     s3_client = S3Client(
#         access_key="7d12f2af5296405f9417d36169d11bc1",
#         secret_key="18afe22c3f2049229a45dc49175983a1",
#         endpoint_url="https://s3.storage.selcloud.ru",
#         bucket_name="barievbucket1",
#     )
#
#     # Проверка, что мы можем загрузить, скачать и удалить файл
#
#     new_file = make_resize(filename)
#
#     # s3_client.upload_file(new_file)

#
# if __name__ == "__main__":
#     make_resize('3333.jpg')
