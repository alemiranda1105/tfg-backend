from pydantic import ValidationError

from app.server.models.Method import NewMethodModel, MethodSchema


def methods_helper(method) -> dict:
    method_dict = {
        "id": str(method["_id"]),
        "user_id": str(method["user_id"]),
        "name": str(method["name"]),
        "info": str(method["info"]),
        "link": str(method["link"]),
        "source_code": "",
        "private": bool(method["private"]),
        "anonymous": bool(method["anonymous"]),
        "results": method["results"]
    }
    if 'source_code' in method:
        method_dict['source_code'] = str(method['source_code'])
    return method_dict


def method_validation_helper(method, method_id, is_new: bool) -> bool:
    try:
        if is_new:
            NewMethodModel(
                name=method['name'],
                user_id=method['user_id'],
                info=method['info'],
                link=method['link'],
                private=method['private'],
                anonymous=method["anonymous"]
            )
        else:
            MethodSchema(
                id=method_id,
                name=method['name'],
                user_id=method['user_id'],
                info=method['info'],
                link=method['link'],
                private=method['private'],
                anonymous=method["anonymous"],
                results=method['results']
            )
    except ValidationError:
        return False
    return True


def users_helper(user):
    return {
        "id": str(user["_id"]),
        "username": str(user["username"])
    }


def user_profile_helper(user):
    return {
        "username": str(user["username"]),
        "email": str(user["email"])
    }


def users_login_helper(user, token: str) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "email": str(user["email"]),
        "token": token
    }
