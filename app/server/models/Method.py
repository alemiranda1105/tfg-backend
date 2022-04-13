from typing import Optional

from pydantic import BaseModel, Field, validator


class NewMethodModel(BaseModel):
    name: str = Field(max_length=25, min_length=3)
    user_id: str = Field(...)
    info: str = Field(max_length=200, min_length=5)
    link: str = Field(max_length=500)
    source_code: Optional[str] = Field(max_length=500)
    private: bool = Field(...)
    anonymous: bool = Field(...)

    @validator('link', allow_reuse=True)
    @validator('source_code', allow_reuse=True)
    def complete_link(cls, v):
        if 'https' not in v or 'http' not in v:
            raise ValueError('URL should be complete')
        return v.title()


class MethodSchema(NewMethodModel):
    id: str = Field(...)
    results: dict = Field(...)
    results_by_category: dict = Field(...)
    results_by_field: list = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": "dasdW231d",
                "user_id": "1",
                "name": "test",
                "info": "This is an example",
                "link": "www.example.com",
                "private": False,
                "anonymous": False,
                "source_code": "www.code.com",
                "results": {
                    "m1": 0.9192,
                    "m2": 0.5421
                }
            }
        }
