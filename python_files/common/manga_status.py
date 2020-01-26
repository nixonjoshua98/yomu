import dataclasses
import typing


@dataclasses.dataclass
class MangaStatus:
	id: int
	text: str
	downloadable: bool


STATUS_TABLE = [
	MangaStatus(0, "Recently Added", downloadable=True),
	MangaStatus(1, "Favourites", downloadable=True),
	MangaStatus(2, "Reading List", downloadable=True),
	MangaStatus(3, "Reading Elsewhere", downloadable=False),
	MangaStatus(4, "Dropped", downloadable=False),
	MangaStatus(5, "Completed", downloadable=False),
]


def from_id(_id: int) -> typing.Union[MangaStatus, None]:
	filtered = list(filter(lambda ele: ele.id == _id, STATUS_TABLE))
	return None if len(filtered) == 0 else filtered[0]


def from_text(txt: str) -> typing.Union[MangaStatus, None]:
	filtered = list(filter(lambda ele: ele.text == txt, STATUS_TABLE))
	return None if len(filtered) == 0 else filtered[0]


def all_text() -> list: return [ele.text for ele in STATUS_TABLE]
def all_ids() -> list: return [ele.id for ele in STATUS_TABLE]
def all_downloadable() -> list: return list(filter(lambda ele: ele.downloadable, STATUS_TABLE))
def all_downloadable_ids() -> list: return [ele.id for ele in all_downloadable()]
