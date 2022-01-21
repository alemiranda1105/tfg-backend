import hashlib

from app.server.database import users_collection
from app.server.helpers.Helpers import users_helper


async def create_user(user):
    user['password'] = hash_password(user['password'])
    u = users_collection.insert_one(user)
    new_user = users_collection.find_one({"_id": u.inserted_id})
    return users_helper(new_user)


def hash_password(password: str) -> str:
    password = hashlib.md5(password.encode('utf-8'))
    return password.hexdigest()
