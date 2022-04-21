from pydantic import ValidationError

from server.models.User import BaseUserSchema, NewUserSchema, LoginUserSchema


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


def user_validation_helper(user, user_id: str, is_new: str) -> bool:
    try:
        if is_new == "sign_up":
            NewUserSchema(
                email=user['email'],
                username=user['username'],
                password=user['password']
            )
        elif is_new == "login":
            if user['email'] is not None:
                LoginUserSchema(
                    email=user['email'],
                    password=user['password']
                )
            elif user['username'] is not None:
                LoginUserSchema(
                    username=user['username'],
                    password=user['password']
                )
            else:
                return False
        elif is_new == "registered":
            BaseUserSchema(
                id=user_id,
                username=user['username'],
                email=user['email'],
                password=user['password'],
                role=user['role']
            )
        else:
            return False
    except ValidationError:
        return False
    return True


