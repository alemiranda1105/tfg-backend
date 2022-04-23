from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from server.database import content_collection
from server.helpers.Content_helper import content_helper, validation_content_helper


def get_all_content():
    content = []
    for c in content_collection.find():
        content.append(content_helper(c))
    return content


def get_content_by_title(title: str):
    content = content_collection.find_one({"title": title})
    if not content:
        return False
    return content_helper(content)


def get_content_by_id(content_id: str):
    content = content_collection.find_one({"_id": content_id})
    if not content:
        return False
    return content_helper(content)


def create_content(content):
    if validation_content_helper(content, True):
        try:
            inserted = content_collection.insert_one(content)
            new_content = content_collection.find_one({"_id": inserted.inserted_id})
            if new_content:
                return content_helper(new_content)
        except DuplicateKeyError:
            return False
    return False


def update_content(content_id: str, content):
    if validation_content_helper(content, True):
        content_id = ObjectId(content_id)
        old = content_collection.find_one({"_id": content_id})
        if old:
            repeated_title = content_collection.find_one({
                "$and": [
                    {"title": content["title"]},
                    {"_id": {
                        "$ne": content_id
                    }}
                ]
            })
            if repeated_title:
                return False

            updated = content_collection.update_one({"_id": content_id}, {"$set": content})
            if updated:
                new_content = content_collection.find_one({"_id": content_id})
                return content_helper(new_content)
    return False


def delete_content(content_id: str):
    content_id = ObjectId(content_id)
    removed = content_collection.delete_one({"_id": content_id})
    return removed.deleted_count >= 1
