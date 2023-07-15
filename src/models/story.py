from bson import ObjectId
from pydantic import Field
from .base_model import BaseModel


class Story(BaseModel):
    id: ObjectId = Field(alias="_id", default_factory=ObjectId)

    title: str
    url: str
    latest_chapter: float = Field(0, alias="latestChapter")
    chapters_read: float = Field(0, alias="latestChapterRead")
    status: int = Field(0, alias="status")
