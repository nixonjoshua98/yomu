from pydantic import BaseModel as _BaseModel, Field
from typing import Union
from src.statuses import StatusList, Status


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
    latest_chapter: Union[int, float] = Field(0, alias="latestChapter")
    chapters_read: Union[int, float] = Field(0, alias="latestChapterRead")
    status_int: int = Field(..., alias="status")

    @property
    def status(self) -> Status:
        return StatusList.get_by_id(self.status_int)
