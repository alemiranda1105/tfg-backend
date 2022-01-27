from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "example@example.com",
                "username": "test_1",
                "password": "daswef123@#2"
            }
        }


class UserLoginSchema(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "test_1",
                "password": "daswef123@#2"
            }
        }


class LoggedUserSchema(BaseModel):
    id: str = Field()
    username: str = Field()
    email: EmailStr = Field()
    token: str = Field()

    class Config:
        schema_extra = {
            "example": {
                "id": "61f12475ba18c90f68911ed3",
                "username": "example",
                "email": "example@example.com",
                "token": "this_is_not_a_token"
            }
        }
