from pymongo import MongoClient
from app import config

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]
input_collection = db[config.MONGO_INPUT_COLLECTION]
output_collection = db[config.MONGO_OUTPUT_COLLECTION]
