
import abc
import enum
import dataclasses

from typing import Union

import manganelo.rewrite as manganelo


class DataSourceType(enum.IntEnum):
    MANGANELO = 0


@dataclasses.dataclass(frozen=True)
class DataSourceChapter:
    title: str = None
    url: str = None

    chapter: Union[int, float] = None


class AbstractDataSource(abc.ABC):

    @abc.abstractmethod
    def get_chapters(self, *, url) -> list[DataSourceChapter]: ...


class _ManganeloDataSource(AbstractDataSource):
    def get_chapters(self, *, url) -> list[DataSourceChapter]:
        try:
            return [DataSourceChapter(c.title, c.url, c.chapter) for c in manganelo.chapter_list(url=url)]
        except manganelo.NotFound:
            return []


ManganeloDataSource = _ManganeloDataSource()
