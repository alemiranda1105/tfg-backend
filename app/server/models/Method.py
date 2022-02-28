from typing import List
from pydantic import BaseModel


class MethodSchema(BaseModel):
    class Result:
        name: str
        res: float

    id: str
    user_id: str
    name: str
    info: str
    link: str
    results: dict

    class Config:
        schema_extra = {
            "example": {
                "id": "dasdW231d",
                "user_id": "1",
                "name": "test",
                "info": "This is an example",
                "link": "www.example.com",
                "results": {
                    "m1": 0.9192,
                    "m2": 0.5421
                }
            }
        }
