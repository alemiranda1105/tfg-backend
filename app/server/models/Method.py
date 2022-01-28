from typing import List
from pydantic import BaseModel, Field


class MethodSchema(BaseModel):
    class Result(BaseModel):
        name: str
        result: float

    id: str
    user_id: str
    name: str
    info: str
    link: str
    results: List

    class Config:
        schema_extra = {
            "example": {
                "id": "dasdW231d",
                "user_id": "1",
                "name": "test",
                "info": "This is an example",
                "link": "www.example.com",
                "results": [
                    {
                        "m1": 0.9192
                    },
                    {
                        "m2": 0.5421
                    }
                ]
            }
        }


class UploadMethodSchema(BaseModel):
    user_id: str = Field(...)
    name: str = Field(...)
    info: str = Field(...)
    link: str = Field(...)
    results: List = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "dasdW231d",
                "user_id": "1",
                "name": "test",
                "info": "This is an example",
                "link": "www.example.com",
                "results": []
            }
        }
