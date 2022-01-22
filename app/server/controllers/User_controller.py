from pymongo.errors import DuplicateKeyError

from app.server.database import users_collection
from app.server.helpers.Helpers import users_helper
from app.server.utils.Utils import hash_password


async def create_user(user):
    user['password'] = hash_password(user['password'])
    try:
        u = users_collection.insert_one(user)
        new_user = users_collection.find_one({"_id": u.inserted_id})
        return users_helper(new_user)
    except DuplicateKeyError:
        return False
