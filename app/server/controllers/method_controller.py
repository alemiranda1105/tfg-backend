from bson import ObjectId

from app.server.database import methods_collection
from app.server.helpers.helpers import methods_helper


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
