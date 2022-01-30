import abc
import dataclasses
from typing import Union

import mangakatana
import manganelo

from src.models import Story


def get_data_source(story: Story):
    source = {
        StoryDataSource.MANGANELO: ManganeloDataSource,
        StoryDataSource.MANGAKATANA: MangakatanaDataSource
    }.get(story.source_id)

    if source is None:
        if any(map(lambda ele: ele in story.url, ("manganelo", "manganato"))):
            return ManganeloDataSource
        else:
            return MangakatanaDataSource

    return source


class StoryDataSource:
    MANGANELO = 0  # Manganato
    MANGAKATANA = 1


@dataclasses.dataclass(frozen=True)
class DataSourceChapter:
    source_id: int

    title: str
    url: str
    chapter: Union[int, float]


@dataclasses.dataclass(frozen=True)
class DataSourceSearchResult:
    source_id: int

    title: str
    url: str
    source_id: int


class AbstractDataSource(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def search(title) -> list[DataSourceSearchResult]: ...

    @staticmethod
    @abc.abstractmethod
    def get_chapters(url) -> list[DataSourceChapter]: ...


class ManganeloDataSource(AbstractDataSource):

    @staticmethod
    def search(title) -> list[DataSourceSearchResult]:
        ls = []

        for ele in manganelo.get_search_results(title):
            ls.append(DataSourceSearchResult(source_id=StoryDataSource.MANGANELO, title=ele.title, url=ele.url))

        return ls[::-1]

    @staticmethod
    def get_chapters(url) -> list[DataSourceChapter]:
        ls = []

        for ele in manganelo.get_chapter_list(url):
            inst = DataSourceChapter(
                source_id=StoryDataSource.MANGANELO,
                chapter=ele.chapter,
                title=ele.title,
                url=ele.url
            )

            ls.append(inst)

        return ls


class MangakatanaDataSource(AbstractDataSource):

    @staticmethod
    def search(title) -> list[DataSourceSearchResult]:
        ls = []

        for ele in mangakatana.search(title=title):
            ls.append(DataSourceSearchResult(source_id=StoryDataSource.MANGAKATANA, title=ele.title, url=ele.url))

        return ls[::-1]

    @staticmethod
    def get_chapters(url) -> list[DataSourceChapter]:
        ls = []

        for ele in mangakatana.chapter_list(url=url):
            ls.append(DataSourceChapter(
                source_id=StoryDataSource.MANGAKATANA,
                chapter=ele.chapter,
                title=ele.title,
                url=ele.url
            ))

        return ls
