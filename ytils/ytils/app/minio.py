from minio import Minio
from minio.error import S3Error
import io

from app.logger import logger
from app.settings import settings


minio_client = Minio(
    endpoint=settings.minio_server_url,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure
)


def save_to_minio(bucket_name: str, object_name: str, file_data: bytes, content_type: str = "application/octet-stream"):
    # Create the bucket if it doesn't exist
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Upload the file
    minio_client.put_object(
        bucket_name,
        object_name,
        io.BytesIO(file_data),
        length=len(file_data),
        content_type=content_type
    )


def check_object(bucket_name: str, object_name: str) -> bool:
    """
    Check to see if an object exists in minio without retrieving the object
    """
    try:
        minio_client.stat_object(bucket_name, object_name)
        return True
    except S3Error as err:
        logger.debug(f"Failed to get object: {err}")
        return False


def get_from_minio(bucket_name: str, object_name: str):
    try:
        response = minio_client.get_object(bucket_name, object_name)
        return response
        # data = response.read()  # Read the full object content into memory
        # response.close()
        # response.release_conn()
        # return data
    except S3Error as err:
        logger.debug(f"Failed to get object: {err}")
        raise err


def list_all_objects(bucket_name: str):
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        return [obj.object_name for obj in objects]
    except Exception as e:
        print(f"Error listing objects: {e}")
        return []
