import abc
import dataclasses
from typing import Union

import mangakatana
import manganelo

from src.data_entities import Story


def get_data_source(story: Story):
    if any(map(lambda ele: ele in story.url, ("manganelo", "manganato"))):
        return ManganeloDataSource

    return MangakatanaDataSource


@dataclasses.dataclass(frozen=True)
class DataSourceChapter:
    title: str
    url: str
    chapter: Union[int, float]


@dataclasses.dataclass(frozen=True)
class DataSourceSearchResult:
    title: str
    url: str


class AbstractDataSource(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def search(title) -> list[DataSourceSearchResult]:
        ...

    @staticmethod
    @abc.abstractmethod
    def get_chapters(url) -> list[DataSourceChapter]:
        ...


class ManganeloDataSource(AbstractDataSource):
    @staticmethod
    def search(title) -> list[DataSourceSearchResult]:
        ls = []

        for ele in manganelo.get_search_results(title):
            ls.append(DataSourceSearchResult(title=ele.title, url=ele.url))

        return ls[::-1]

    @staticmethod
    def get_chapters(url) -> list[DataSourceChapter]:
        ls = []

        for ele in manganelo.get_chapter_list(url):
            inst = DataSourceChapter(chapter=ele.chapter, title=ele.title, url=ele.url)

            ls.append(inst)

        return ls


class MangakatanaDataSource(AbstractDataSource):
    @staticmethod
    def search(title) -> list[DataSourceSearchResult]:
        ls = []

        for ele in mangakatana.search(title=title):
            ls.append(DataSourceSearchResult(title=ele.title, url=ele.url))

        return ls[::-1]

    @staticmethod
    def get_chapters(url) -> list[DataSourceChapter]:
        ls = []

        for ele in mangakatana.chapter_list(url=url):
            ls.append(
                DataSourceChapter(chapter=ele.chapter, title=ele.title, url=ele.url)
            )

        return ls
