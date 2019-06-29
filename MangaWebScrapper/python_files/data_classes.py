import dataclasses


@dataclasses.dataclass(init=False)
class MangaDataClass:
	title: str
	desc: str
	url: str
	chapter: float


@dataclasses.dataclass(init=False)
class MangaSearchResult:
	title: str
	url: str
	desc: str