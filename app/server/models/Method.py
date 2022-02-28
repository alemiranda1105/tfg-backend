from pydantic import BaseModel, Field


class NewMethodModel(BaseModel):
    name: str = Field(max_length=25, min_length=3)
    user_id: str = Field(...)
    info: str = Field(max_length=200, min_length=5)
    link: str = Field(max_length=50, min_length=3)


class MethodSchema(BaseModel):
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
