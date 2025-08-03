import logging
from app.mongo_client import input_collection, output_collection
from app.minio_client import minio_client
from app.models.metadata_model import DocumentModel
from app.config import settings
from bs4 import BeautifulSoup
import hashlib
import os
import io
from minio.error import S3Error

logger = logging.getLogger(__name__)



def transform_file(file_bytes: bytes, ref_no: str) -> tuple[str, bytes, str]:
    soup = BeautifulSoup(file_bytes, 'html.parser')

    # Precise selection: container -> inner container -> row -> col-sm-9
    container = soup.select_one('div.container.mb-4 div.container div.row div.col-sm-9')

    if container:
        content_html = container.prettify()
    else:
        content_html = '<div>No content found</div>'

    transformed_bytes = content_html.encode('utf-8')
    new_hash = hashlib.md5(transformed_bytes).hexdigest()
    new_name = f"{ref_no}.html"

    return new_name, transformed_bytes, new_hash




def run_transformation(start_date: str, end_date: str):
    logger.info(f"[DEBUG] Received start_date={repr(start_date)}, end_date={repr(end_date)}")


    query = {
        "partition_date": {
            "$gte": start_date,
            "$lte": end_date
        }
    }
    

    documents = list(input_collection.find(query))
    documents_count = len(documents)
    logger.info(f"[QUERY] Mongo returned {len(documents)} documents")

    if not documents:
        logger.info("[EMPTY] No documents found for the given date range")
        return

    for doc in documents:
        model = DocumentModel(**doc)
        try:
            file_obj = minio_client.get_object(
                settings.MINIO_SOURCE_BUCKET, model.file_path)
            file_data = file_obj.read()
        except S3Error as e:
            logger.error(f"[SKIP] MinIO file not found: {model.file_path} — {e.code}")
            continue

        ext = os.path.splitext(model.file_path)[1].lower()
        if ext == '.html':
            new_name, new_data, new_hash = transform_file(
                file_data, model.ref_no)
            model.file_hash = new_hash
            object_path = f"{model.partition_date}/{new_name}"
            minio_client.put_object(
                settings.MINIO_TARGET_BUCKET,
                object_path,
                data=io.BytesIO(new_data),
                length=len(new_data)
            )
            logger.info(
                f"Transformed HTML file {model.file_path}, new length: {len(new_data)}")
        else:
            object_path = f"{model.partition_date}/{model.ref_no}{ext}"
            minio_client.put_object(
                settings.MINIO_TARGET_BUCKET,
                object_path,
                data=io.BytesIO(file_data),
                length=len(file_data)
            )
            logger.info(
                f"Copied non-HTML file {model.file_path}, size: {len(file_data)}")

        model.file_path = object_path
        output_collection.insert_one(model.dict())
        logger.info(
            f"Inserted transformed document for ref_no {model.ref_no} into output collection")

    return documents_count