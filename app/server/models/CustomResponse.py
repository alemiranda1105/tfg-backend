

def error_response(msg: str) -> dict:
    return {
        "Error": "{}".format(msg)
    }
