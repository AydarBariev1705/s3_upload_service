from io import BytesIO

from PIL import Image
from main.s3client import S3Client
from main.config import ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, BUCKET_NAME


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
