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
