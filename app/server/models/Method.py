from typing import List

from pydantic import BaseModel, Field


class MethodSchema(BaseModel):
    class Result(BaseModel):
        name: str = Field(...)
        result: float = Field(...)

    user_id: str = Field(...)
    name: str = Field(...)
    info: str = Field(...)
    link: str = Field(...)
    results: List[Result] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "1",
                "name": "test",
                "info": "This is an example",
                "link": "www.example.com",
                "results": [
                    {
                        "name": "m1",
                        "result": 0.9192
                    },
                    {
                        "name": "m2",
                        "result": 0.5421
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
                "user_id": "1",
                "name": "test",
                "info": "This is an example",
                "link": "www.example.com",
                "results": []
            }
        }
