import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://ramirami:rami123@mongodb:27017")
MONGO_DB = os.environ.get("MONGO_DB", "kedra")
MONGO_INPUT_COLLECTION = os.environ.get("MONGO_INPUT_COLLECTION", "workplace")
MONGO_OUTPUT_COLLECTION = os.environ.get("MONGO_OUTPUT_COLLECTION", "transformed_documents")

MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
MINIO_SOURCE_BUCKET = os.environ.get("MINIO_SOURCE_BUCKET", "workplace")
MINIO_TARGET_BUCKET = os.environ.get("MINIO_TARGET_BUCKET", "workplace-transformed")
MINIO_TRANSFORMED_URL = os.environ.get("MINIO_TRANSFORMED_URL", "http://localhost:9090/browser/workplace-transformed/")
