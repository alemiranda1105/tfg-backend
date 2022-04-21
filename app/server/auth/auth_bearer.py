from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from server.auth.auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid auth. scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid auth. code")

    def verify_jwt(self, token: str) -> bool:
        token_valid: bool = False
        try:
            payload = decode_jwt(token)
        except:
            payload = None
        if payload:
            token_valid = True
        return token_valid
