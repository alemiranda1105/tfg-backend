import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv('DATABASE')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client.tfg
