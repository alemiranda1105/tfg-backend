from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from server.database import methods_collection
from server.evaluation.evaluation import evaluation
from server.helpers.Methods_Helper import methods_helper, method_validation_helper
from server.utils.Utils import to_csv, to_xls


def find_all(user_id: str = ""):
    methods = []
    for m in methods_collection.find():
        if not m['private'] or m['user_id'] == user_id:
            if m['anonymous'] and m['user_id'] != user_id:
                m['user_id'] = ""
            methods.append(methods_helper(m))
    return methods


def find_by_id(method_id, user_id: str = ""):
    try:
        method = methods_collection.find_one({"_id": ObjectId(method_id)})
    except:
        return False
    if not method:
        return False
    if method['user_id'] != user_id:
        if method['private']:
            return False
        if method['anonymous'] and method['user_id'] != user_id:
            method['user_id'] = ""
    return methods_helper(method)


def find_by_user_id(user_id, token_id):
    methods = []
    for m in methods_collection.find({"user_id": user_id}):
        if token_id != user_id:
            if not m['private']:
                if m['anonymous'] and m['user_id'] != user_id:
                    m['user_id'] = ""
                methods.append(methods_helper(m))
        elif token_id == user_id:
            methods.append((methods_helper(m)))
    if len(methods) <= 0:
        return False
    return methods


def create_method(method, method_file):
    if not method_validation_helper(method, "", True):
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


def update_method(method_id, method, user_id):
    if not method_validation_helper(method, "", True):
        return False

    try:
        del method['id']
        del method['results']
        del method['results_by_category']
        del method['results_by_category_field']
        del method['results_by_field']
    except:
        pass

    method_id = ObjectId(method_id)
    old = methods_collection.find_one({"_id": method_id})
    if old:
        if old['user_id'] != user_id:
            return False
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


def update_and_evaluate(method_id, method, file, user_id):
    if not method_validation_helper(method, method_id, True):
        return False

    try:
        del method['id']
        del method['results']
        del method['results_by_category']
        del method['results_by_category_field']
        del method['results_by_field']
    except:
        pass

    method_id = ObjectId(method_id)
    old = methods_collection.find_one({"_id": method_id})
    if old:
        if old['user_id'] != user_id:
            return False
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


def delete_method(method_id, user_id):
    method_id = ObjectId(method_id)
    old = methods_collection.find_one({"_id": method_id})
    if old:
        if old['user_id'] != user_id:
            return False
    removed = methods_collection.delete_one({"_id": method_id})
    return removed.deleted_count >= 1


def delete_by_user_id(user_id, token_id):
    if find_by_user_id(user_id, token_id):
        removed = methods_collection.delete_many({"user_id": user_id})
        return removed.deleted_count >= 1
    return True


def download_all_methods(file_type, user_id: str = ""):
    methods = find_all(user_id)
    if len(methods) <= 0:
        return False
    if file_type == "json":
        return methods
    elif file_type == "csv":
        return to_csv(methods)
    elif file_type == "xls":
        return to_xls(methods)


def download_method_files(method_id: str, user_id: str):
    method_id = ObjectId(method_id)
    method = methods_collection.find_one({"_id": method_id})
    if method:
        if method['user_id'] == user_id:
            return method['file_dir'] + '.zip'
    return False


def evaluate_method(method, file):
    method = evaluation(method, file)
    return method
