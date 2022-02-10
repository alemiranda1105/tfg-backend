from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.server.auth.auth_handler import sign_jwt
from app.server.database import users_collection
from app.server.helpers.Helpers import users_helper, users_login_helper
from app.server.utils.Utils import hash_password


def find_user_by_id(user_id: str):
    u_id = ObjectId(user_id)
    user = users_collection.find_one({"_id": u_id})
    if user:
        return users_helper(user)
    return False


async def create_user(user):
    user['password'] = hash_password(user['password'])
    try:
        u = users_collection.insert_one(user)
        new_user = users_collection.find_one({"_id": u.inserted_id})
        return users_login_helper(new_user, sign_jwt(str(new_user['_id']))['token'])
    except DuplicateKeyError:
        return False


async def verify_user(user):
    user['password'] = hash_password(user['password'])
    if user['username'] is not None:
        u = users_collection.find_one({"username": user['username']})
        if u is not None:
            if u['password'] == user['password']:
                return users_login_helper(u, sign_jwt(str(u['_id']))['token'])
    if user['email'] is not None:
        u = users_collection.find_one({"email": user['email']})
        if u is not None:
            if u['password'] == user['password']:
                return users_login_helper(u, sign_jwt(str(u['_id']))['token'])
    return False
