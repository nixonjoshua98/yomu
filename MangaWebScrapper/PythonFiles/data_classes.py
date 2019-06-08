import dataclasses


@dataclasses.dataclass(init=False)
class SearchResult:
	title: str
	desc: float
	url: str


@dataclasses.dataclass(init=False)
class MangaChapter:
	chapter_num: float
	url: str


@dataclasses.dataclass(init=True)
class DownloadQueueRow:
	title: str
	chapter: float