from bson import ObjectId

from app.server.database import methods_collection
from app.server.helpers.Helpers import methods_helper


async def find_all():
    methods = []
    for m in methods_collection.find():
        methods.append(methods_helper(m))
    return methods


async def find_by_id(method_id):
    method = methods_collection.find_one({"_id": ObjectId(method_id)})
    if not method:
        return False
    return methods_helper(method)


async def find_by_user_id(user_id):
    methods = []
    for m in methods_collection.find({"user_id": user_id}):
        methods.append(methods_helper(m))
    if len(methods) <= 0:
        return False
    return methods


async def create_method(method):
    m = methods_collection.insert_one(method)
    new_method = methods_collection.find_one({"_id": m.inserted_id})
    return methods_helper(new_method)


async def update_method(method_id, method):
    method_id = ObjectId(method_id)
    old = methods_collection.find_one({"_id": method_id})
    if old:
        updated = methods_collection.update_one({"_id": method_id}, {"$set": method})
        if updated:
            new_method = methods_collection.find_one({"_id": method_id})
            return methods_helper(new_method)
    return False
