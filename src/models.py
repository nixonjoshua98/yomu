from bson import ObjectId

from pydantic import BaseModel as _BaseModel
from pydantic import Field


class BaseModel(_BaseModel):

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = True

        return super().dict(**kwargs)


class Story(BaseModel):
    id: ObjectId = Field(alias="_id", default_factory=ObjectId)

    title: str
    url: str
    latest_chapter: float = Field(0, alias="latestChapter")
    chapters_read: float = Field(0, alias="latestChapterRead")
    status: int = Field(0, alias="status")
