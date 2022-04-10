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
        "results": method["results"],
        "results_by_category": method["results_by_category"]
    }
    if 'source_code' in method:
        method_dict['source_code'] = str(method['source_code'])
    return method_dict


def method_validation_helper(method, method_id, is_new: bool) -> bool:
    try:
        if is_new:
            if 'source_code' in method:
                NewMethodModel(
                    name=method['name'],
                    user_id=method['user_id'],
                    info=method['info'],
                    link=method['link'],
                    source_code=method['source_code'],
                    private=method['private'],
                    anonymous=method["anonymous"]
                )
            else:
                NewMethodModel(
                    name=method['name'],
                    user_id=method['user_id'],
                    info=method['info'],
                    link=method['link'],
                    private=method['private'],
                    anonymous=method["anonymous"]
                )
        else:
            if 'source_code' in method:
                MethodSchema(
                    id=method_id,
                    name=method['name'],
                    user_id=method['user_id'],
                    info=method['info'],
                    link=method['link'],
                    source_code=method['source_code'],
                    private=method['private'],
                    anonymous=method["anonymous"],
                    results=method['results'],
                    results_by_category=method["results_by_category"]
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
                    results=method['results'],
                    results_by_category=method["results_by_category"]
                )
    except ValidationError:
        return False
    return True
