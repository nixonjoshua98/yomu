from pydantic import BaseModel as _BaseModel
from pydantic import Field
from src import utils
import datetime as dt

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
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    def dict(self, *args, **kwargs):
        kwargs["by_alias"] = True

        return super().dict(**kwargs)


class Story(BaseModel):
    id: str = Field(..., alias="storyId")
    title: str
    url: str
    latest_chapter: NumberField = Field(0, alias="latestChapter")
    chapters_read: NumberField = Field(0, alias="latestChapterRead")
    status_value: int = Field(..., alias="status")
    last_missing_story_check: dt.datetime = Field(None, alias="lastMissingStoryCheck")

    def can_update_missing_story(self) -> bool:
        return self.last_missing_story_check is None or (utils.utcnow() - self.last_missing_story_check).days >= 1
