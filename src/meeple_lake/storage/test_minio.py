from pathlib import Path

from minio_client import (
    get_minio_client,
    ensure_bucket,
    upload_file,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

xml_file = (
    PROJECT_ROOT
    / "data"
    / "bronze"
    / "bgg"
    / "thing"
    / "batch_0001_2026-09-02.xml"
)

client = get_minio_client()

ensure_bucket(client)

upload_file(
    client=client,
    local_path=xml_file,
    object_name="bronze/bgg/thing/test_batch.xml",
)

print("Upload concluído")