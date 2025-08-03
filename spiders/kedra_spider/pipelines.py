import os
import io
import requests
from datetime import datetime
from pymongo import MongoClient
from itemadapter import ItemAdapter
from minio import Minio
from minio.error import S3Error
import hashlib


class MongoMetadataPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection,
                 minio_endpoint, minio_access_key, minio_secret_key, bucket_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.minio_endpoint = minio_endpoint
        self.minio_access_key = minio_access_key
        self.minio_secret_key = minio_secret_key
        self.bucket_name = bucket_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI", "mongodb://ramirami:rami123@mongodb:27017"),
            mongo_db=crawler.settings.get("MONGO_DB", "kedra"),
            mongo_collection=crawler.settings.get("MONGO_COLLECTION", "workplace"),
            minio_endpoint=crawler.settings.get("MINIO_ENDPOINT", "minio:9000"),
            minio_access_key=crawler.settings.get("MINIO_ACCESS_KEY", "minio"),
            minio_secret_key=crawler.settings.get("MINIO_SECRET_KEY", "minio123"),
            bucket_name=crawler.settings.get("MINIO_BUCKET", "workplace")
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

        self.minio_client = Minio(
            self.minio_endpoint,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False
        )

        if not self.minio_client.bucket_exists(self.bucket_name):
            self.minio_client.make_bucket(self.bucket_name)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        date_str = adapter.get("date")  # format: '18/07/2025'
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        partition_date = date_obj.replace(day=1).strftime("%Y-%m-%d")

        ref_no = adapter.get("ref_no")
        link = adapter.get("link")
        extension = "html" if link.endswith(".html") else link.split(".")[-1]
        file_path = f"{partition_date}/{ref_no}.{extension}"

        try:
            response = requests.get(link)
            response.raise_for_status()
            content = response.content

            file_hash = hashlib.md5(content).hexdigest()

            self.minio_client.put_object(
                bucket_name=self.bucket_name,
                object_name=file_path,
                data=io.BytesIO(content),
                length=len(content),
                content_type="text/html"
            )

            metadata_doc = adapter.asdict()
            metadata_doc["partition_date"] = partition_date
            metadata_doc["file_path"] = file_path
            metadata_doc["file_hash"] = file_hash

            result = self.collection.insert_one(metadata_doc)
            spider.logger.info(f"Inserted document with _id={result.inserted_id}")

        except Exception as e:
            spider.logger.error(f"Error in processing item: {e}")

        return item
