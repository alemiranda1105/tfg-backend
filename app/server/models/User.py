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
