import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv('DATABASE')
client = pymongo.MongoClient(MONGO_DETAILS)

db = client['tfg']

methods_collection = db["methods"]


def methods_helper(method) -> dict:
    return {
        "id": str(method["_id"]),
        "user_id": str(method["user_id"]),
        "name": str(method["name"]),
        "info": str(method["info"]),
        "link": str(method["link"]),
        "results": method["results"]
    }
