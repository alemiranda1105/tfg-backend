from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError

from app.server.auth.auth_handler import sign_jwt
from app.server.database import users_collection
from app.server.helpers.Users_Helper import users_helper, users_login_helper, user_profile_helper
from app.server.models.User import UserSchema
from app.server.utils.Utils import hash_password


def find_user_by_id(user_id: str):
    u_id = ObjectId(user_id)
    user = users_collection.find_one({"_id": u_id})
    if user:
        return users_helper(user)
    return False


def get_user_profile(user_id: str):
    u_id = ObjectId(user_id)
    user = users_collection.find_one({"_id": u_id})
    if user:
        return user_profile_helper(user)
    return False


async def create_user(user):
    try:
        UserSchema(
            email=user['email'],
            username=user['username'],
            password=user['password']
        )
    except ValidationError:
        return False

    user['password'] = hash_password(user['password'])
    try:
        u = users_collection.insert_one(user)
        new_user = users_collection.find_one({"_id": u.inserted_id})
        return users_login_helper(new_user, sign_jwt(str(new_user['_id']))['token'])
    except DuplicateKeyError:
        return False


async def verify_user(user):
    user['password'] = hash_password(user['password'])
    found = users_collection.find_one({
        "$or": [
            {"username": user['username']},
            {"email": user['email']}
        ]
    })
    if found:
        if found['password'] == user['password']:
            return users_login_helper(found, sign_jwt(str(found['_id']))['token'])
    return False


# Only updates username and/or email
def update_user(user_id: str, user_data):
    try:
        UserSchema(
            email=user_data['email'],
            username=user_data['username'],
            password=user_data['password']
        )
    except ValidationError:
        return False

    user_data['password'] = hash_password(user_data['password'])
    user_id = ObjectId(user_id)
    old = users_collection.find_one({"_id": user_id})
    if old:
        if old['password'] != user_data['password']:
            return False
        repeated_username = users_collection.find_one(
            {"$and": [
                {"username": user_data['username']},
                {"_id": {
                    "$ne": user_id
                }}
            ]}
        )
        repeated_email = users_collection.find_one(
            {"$and": [
                {"email": user_data['email']},
                {"_id": {
                    "$ne": user_id
                }}
            ]}
        )
        if repeated_email or repeated_username:
            return False

        updated = users_collection.update_one({"_id": user_id}, {"$set": user_data})
        if updated:
            new_user_data = users_collection.find_one({"_id": user_id})
            return user_profile_helper(new_user_data)
    return False


def delete_user(user_id):
    user_id = ObjectId(user_id)
    removed = users_collection.delete_one({"_id": user_id})
    return removed.deleted_count >= 1
