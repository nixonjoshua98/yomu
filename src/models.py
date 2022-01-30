from bson import ObjectId

from pydantic import BaseModel as _BaseModel
from pydantic import Field


class NumberField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        float_v = float(v)
        int_v = int(v)

        if float_v == int_v:
            return int_v

        return float_v


class BaseModel(_BaseModel):

    class Config:
        allow_population_by_field_name = True

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = True

        return super().dict(**kwargs)


class Story(BaseModel):
    id: str = Field(alias="storyId", default_factory=lambda: str(ObjectId()))

    title: str
    url: str
    source_id: int = Field(None, alias="sourceId")
    latest_chapter: NumberField = Field(0, alias="latestChapter")
    chapters_read: NumberField = Field(0, alias="latestChapterRead")
    status_value: int = Field(..., alias="status")
