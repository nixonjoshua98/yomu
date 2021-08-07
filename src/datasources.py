
import abc
import dataclasses

from typing import Union

import manganelo.rewrite as manganelo
import mangakatana


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
    def search(self, url) -> list[DataSourceSearchResult]: ...

    @abc.abstractmethod
    def get_chapters(self, url) -> list[DataSourceChapter]: ...


class _ManganeloDataSource(AbstractDataSource):

    def search(self, title) -> list[DataSourceSearchResult]:
        return [DataSourceSearchResult(res.title, res.url) for res in manganelo.search(title=title)]

    def get_chapters(self, url) -> list[DataSourceChapter]:
        return [DataSourceChapter(c.title, c.url, c.chapter) for c in manganelo.chapter_list(url=url)]


class _MangaKatanaDataSource(AbstractDataSource):

    def search(self, title) -> list[DataSourceSearchResult]:
        return [DataSourceSearchResult(res.title, res.url) for res in mangakatana.search(title=title)]

    def get_chapters(self, url) -> list[DataSourceChapter]:
        try:
            return [DataSourceChapter(c.title, c.url, c.chapter) for c in mangakatana.chapter_list(url=url)]
        except manganelo.NotFound:
            return []


ManganeloDataSource = _ManganeloDataSource()
MangaKatanaDataSource = _MangaKatanaDataSource()
