import sys
import os

import pymongo
from dotenv import load_dotenv

load_dotenv()

if 'pytest' in sys.argv[0]:
    MONGO_DETAILS = os.getenv('DATABASE_TEST')
    client = pymongo.MongoClient(MONGO_DETAILS)
    db = client['tfg_test']
else:
    MONGO_DETAILS = os.getenv('DATABASE')
    client = pymongo.MongoClient(MONGO_DETAILS)
    db = client['tfg']

methods_collection = db["methods"]
