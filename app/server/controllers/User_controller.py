from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.server.auth.auth_handler import sign_jwt
from app.server.database import users_collection
from app.server.helpers.Users_Helper import users_helper, users_login_helper, user_profile_helper, \
    user_validation_helper
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
        if user_validation_helper(user, user_id, "registered"):
            return user_profile_helper(user)
    return False


async def create_user(user):
    if user_validation_helper(user, "", "sign_up"):
        user['password'] = hash_password(user['password'])
        user['role'] = "user"
        try:
            u = users_collection.insert_one(user)
            new_user = users_collection.find_one({"_id": u.inserted_id})
            return users_login_helper(new_user, sign_jwt(str(new_user['_id']), str(new_user['role']))['token'])
        except DuplicateKeyError:
            return False
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
        if user_validation_helper(user, str(found['_id']), "login"):
            if found['password'] == user['password']:
                return users_login_helper(found, sign_jwt(str(found['_id']), found['role'])['token'])
    return False


# Only updates username and/or email
def update_user(user_id: str, user_data):
    if user_validation_helper(user_data, user_id, "signup"):
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
                if user_validation_helper(updated, str(user_id), "registered"):
                    new_user_data = users_collection.find_one({"_id": user_id})
                    return user_profile_helper(new_user_data)
    return False


def delete_user(user_id):
    user_id = ObjectId(user_id)
    removed = users_collection.delete_one({"_id": user_id})
    return removed.deleted_count >= 1
