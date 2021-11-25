import abc
import dataclasses
from typing import Union

import mangakatana
import manganelo

from src.errors import StoryNotFound


@dataclasses.dataclass(frozen=True)
class DataSourceChapter:
    title: str = None
    url: str = None

    chapter: Union[int, float] = None


@dataclasses.dataclass(frozen=True)
class DataSourceSearchResult:
    title: str
    url: str


class AbstractDataSource(abc.ABC):
    @abc.abstractmethod
    def search(self, title) -> list[DataSourceSearchResult]:
        ...

    @abc.abstractmethod
    def get_chapters(self, url) -> list[DataSourceChapter]:
        ...


class _ManganeloDataSource(AbstractDataSource):
    def search(self, title) -> list[DataSourceSearchResult]:
        return [
            DataSourceSearchResult(res.title, res.url)
            for res in manganelo.get_search_results(title)
        ][::-1]

    def get_chapters(self, url) -> list[DataSourceChapter]:
        try:
            return [
                DataSourceChapter(c.title, c.url, c.chapter)
                for c in manganelo.get_chapter_list(url)
            ]
        except manganelo.NotFound:
            raise StoryNotFound()


class _MangaKatanaDataSource(AbstractDataSource):
    def search(self, title) -> list[DataSourceSearchResult]:
        return [
            DataSourceSearchResult(res.title, res.url)
            for res in mangakatana.search(title=title)
        ][::-1]

    def get_chapters(self, url) -> list[DataSourceChapter]:
        return [
            DataSourceChapter(c.title, c.url, c.chapter)
            for c in mangakatana.chapter_list(url=url)
        ]


ManganeloDataSource = _ManganeloDataSource()
MangaKatanaDataSource = _MangaKatanaDataSource()
