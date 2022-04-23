from pydantic import BaseModel, Field


class ContentSchema(BaseModel):
    id: str = Field(...)
    title: str = Field(...)
    text: str = Field(...)


class NewContentSchema(BaseModel):
    title: str = Field(...)
    text: str = Field(...)
