from datetime import datetime

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from server.database import changelog_collection
from server.helpers.Changelog_helper import changelog_helper, validation_changelog_helper
from server.models.Changelog import BaseChangelogSchema


def get_all_changelog():
    changelog_list = []
    for c in changelog_collection.find():
        changelog_list.append(c)
    changelog_list.sort(key=lambda cl: datetime.strptime(cl['date'], '%d/%m/%Y'))
    changelog_list.reverse()
    sorted_list = []
    for c in changelog_list:
        sorted_list.append(changelog_helper(c))
    return sorted_list


def get_changelog_by_id(changelog_id: str):
    changelog = changelog_collection.find_one({"_id": changelog_id})
    if not changelog:
        return False
    return changelog_helper(changelog)


def create_changelog(changelog: BaseChangelogSchema):
    if validation_changelog_helper(changelog, True):
        try:
            inserted = changelog_collection.insert_one(changelog)
            new_content = changelog_collection.find_one({"_id": inserted.inserted_id})
            if new_content:
                return changelog_helper(new_content)
        except DuplicateKeyError:
            return False
    return False


def update_changelog(changelog_id, changelog):
    if validation_changelog_helper(changelog, True):
        changelog_id = ObjectId(changelog_id)
        old = changelog_collection.find_one({"_id": changelog_id})
        if old:
            updated = changelog_collection.update_one({"_id": changelog_id}, {"$set": changelog})
            if updated:
                new_content = changelog_collection.find_one({"_id": changelog_id})
                return changelog_helper(new_content)
    return False


def delete_changelog(changelog_id: str):
    changelog_id = ObjectId(changelog_id)
    removed = changelog_collection.delete_one({"_id": changelog_id})
    return removed.deleted_count >= 1
