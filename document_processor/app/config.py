from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://ramirami:rami123@mongodb:27017"
    MONGO_DB: str = "kedra"
    MONGO_INPUT_COLLECTION: str = "workplace"
    MONGO_OUTPUT_COLLECTION: str = "transformed_documents"

    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SOURCE_BUCKET: str = "workplace"
    MINIO_TARGET_BUCKET: str = "workplace-transformed"

    class Config:
        env_file = ".env"

settings = Settings()

# For direct imports (as your code tries to do)
MONGO_URI = settings.MONGO_URI
MONGO_DB = settings.MONGO_DB
MONGO_INPUT_COLLECTION = settings.MONGO_INPUT_COLLECTION
MONGO_OUTPUT_COLLECTION = settings.MONGO_OUTPUT_COLLECTION

MINIO_ENDPOINT = settings.MINIO_ENDPOINT
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
MINIO_SOURCE_BUCKET = settings.MINIO_SOURCE_BUCKET
MINIO_TARGET_BUCKET = settings.MINIO_TARGET_BUCKET
