from pymongo import MongoClient
from .config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]
input_collection = db[settings.MONGO_INPUT_COLLECTION]
output_collection = db[settings.MONGO_OUTPUT_COLLECTION]
