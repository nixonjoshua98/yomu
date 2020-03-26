import typing

from dataclasses import dataclass


@dataclass(frozen=True)
class MangaStatus:
	id: int
	text: str
	downloadable: bool


_STATUS_TABLE = [
	MangaStatus(0, "Recently Added", downloadable=True),
	MangaStatus(1, "Favourites", downloadable=True),
	MangaStatus(2, "Reading List", downloadable=True),
	MangaStatus(3, "Reading Elsewhere", downloadable=False),
	MangaStatus(4, "Dropped", downloadable=False),
	MangaStatus(5, "Completed", downloadable=False),
]


def all_text() -> typing.Tuple: return tuple(map(lambda s: s.text, _STATUS_TABLE))
def index2status(index: int) -> MangaStatus: return _STATUS_TABLE[index]
