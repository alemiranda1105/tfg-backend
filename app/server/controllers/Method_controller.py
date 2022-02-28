from bson import ObjectId
from pydantic import ValidationError

from pymongo.errors import DuplicateKeyError

from app.server.database import methods_collection
from app.server.evaluation.evaluation import evaluation
from app.server.helpers.Helpers import methods_helper
from app.server.models.Method import MethodSchema, NewMethodModel
from app.server.utils.Utils import to_csv, to_xls


def find_all():
    methods = []
    for m in methods_collection.find():
        methods.append(methods_helper(m))
    return methods


def find_by_id(method_id):
    method = methods_collection.find_one({"_id": ObjectId(method_id)})
    if not method:
        return False
    return methods_helper(method)


def find_by_user_id(user_id):
    methods = []
    for m in methods_collection.find({"user_id": user_id}):
        methods.append(methods_helper(m))
    if len(methods) <= 0:
        return False
    return methods


def create_method(method, method_file):
    print(method)
    try:
        NewMethodModel(
            name=method['name'],
            user_id=method['user_id'],
            info=method['info'],
            link=method['link']
        )
    except ValidationError:
        return False
    try:
        if methods_collection.find_one({"name": method['name']}):
            raise DuplicateKeyError('El valor ya existe')
        method = evaluate_method(method, method_file)
        m = methods_collection.insert_one(method)
        new_method = methods_collection.find_one({"_id": m.inserted_id})
        return methods_helper(new_method)
    except DuplicateKeyError:
        return False


def update_method(method_id, method):
    method_id = ObjectId(method_id)

    try:
        MethodSchema(
            id=method_id,
            name=method['name'],
            user_id=method['user_id'],
            info=method['info'],
            link=method['link'],
            results=method['results']
        )
    except ValidationError:
        return False

    old = methods_collection.find_one({"_id": method_id})
    if old:
        exists = methods_collection.find_one(
            {"$and": [
                {"name": method['name']},
                {"_id": {
                    "$ne": method_id
                }}
            ]}
        )
        if exists:
            return False
        updated = methods_collection.update_one({"_id": method_id}, {"$set": method})
        if updated:
            new_method = methods_collection.find_one({"_id": method_id})
            return methods_helper(new_method)
    return False


def update_and_evaluate(method_id, method, file):
    method_id = ObjectId(method_id)

    try:
        MethodSchema(
            id=method_id,
            name=method['name'],
            user_id=method['user_id'],
            info=method['info'],
            link=method['link'],
            results=method['results']
        )
    except ValidationError:
        return False

    old = methods_collection.find_one({"_id": method_id})
    if old:
        exists = methods_collection.find_one(
            {"$and": [
                {"name": method['name']},
                {"_id": {
                    "$ne": method_id
                }}
            ]}
        )
        if exists:
            return False
        method = evaluate_method(method, file)
        updated = methods_collection.update_one({"_id": method_id}, {"$set": method})
        if updated:
            new_method = methods_collection.find_one({"_id": method_id})
            return methods_helper(new_method)
    return False


def delete_method(method_id):
    method_id = ObjectId(method_id)
    removed = methods_collection.delete_one({"_id": method_id})
    return removed.deleted_count >= 1


def download_all_methods(file_type):
    methods = find_all()
    if len(methods) <= 0:
        return False
    if file_type == "json":
        return methods
    elif file_type == "csv":
        return to_csv(methods)
    elif file_type == "xls":
        return to_xls(methods)


def evaluate_method(method, file):
    method = evaluation(method, file)
    return method
