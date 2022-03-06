import os
import time
from typing import Dict

import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET")
ALG = os.getenv("JWT_ALG")


def token_response(token: str):
    return {
        "token": token
    }


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 604800
    }
    token = jwt.encode(payload, SECRET, algorithm=ALG)
    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=[ALG])
        if decoded_token['expires'] <= time.time():
            raise Exception('not valid token')
        return decoded_token
    except:
        return {}


def get_id_from_token(token: str):
    payload = decode_jwt(token)
    if 'user_id' in payload:
        return payload['user_id']
    return ''
