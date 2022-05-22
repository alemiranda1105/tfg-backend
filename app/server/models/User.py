from typing import Optional

from pydantic import BaseModel, Field, EmailStr, validator


class BaseUserSchema(BaseModel):
    id: str = Field(...)
    role: str = Field(...)
    email: EmailStr = Field(...)
    username: str = Field(max_length=20, min_length=3)
    password: str = Field(min_length=6)

    @validator('role')
    def valid_role(cls, role):
        if role not in ['admin', 'user']:
            raise ValueError("Not valid role")
        return role


class NewUserSchema(BaseModel):
    email: EmailStr = Field(...)
    username: str = Field(max_length=20, min_length=3)
    password: str = Field(min_length=6)


class LoginUserSchema(BaseModel):
    data: str = Field(...)
    password: str = Field(...)
