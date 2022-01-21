from app.server.database import users_collection
from app.server.helpers.Helpers import users_helper


async def create_user(user):
    u = users_collection.insert_one(user)
    new_user = users_collection.find_one({"_id": u.inserted_id})
    return users_helper(new_user)
