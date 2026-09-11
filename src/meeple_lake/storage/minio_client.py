import os
from pathlib import Path

from dotenv import load_dotenv
from minio import Minio


load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")


def get_minio_client() -> Minio:
    return Minio(
        endpoint=MINIO_ENDPOINT,
        access_key=MINIO_ROOT_USER,
        secret_key=MINIO_ROOT_PASSWORD,
        secure=False,
    )


def ensure_bucket(client: Minio) -> None:
    if not client.bucket_exists(MINIO_BUCKET):
        client.make_bucket(MINIO_BUCKET)


def upload_file(
    client: Minio,
    local_path: Path,
    object_name: str,
) -> None:

    client.fput_object(
        bucket_name=MINIO_BUCKET,
        object_name=object_name,
        file_path=str(local_path),
    )