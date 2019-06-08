import dataclasses


@dataclasses.dataclass(init=False)
class SearchResult:
	title: str
	desc: float
	url: str


@dataclasses.dataclass(init=False)
class MangaChapter:
	# title: str
	chapter_num: float
	url: str
