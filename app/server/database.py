import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv('DATABASE')
client = pymongo.MongoClient(MONGO_DETAILS)

db = client['tfg']

methods_collection = db["methods"]
