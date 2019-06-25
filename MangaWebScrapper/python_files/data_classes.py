import dataclasses


@dataclasses.dataclass(init=False)
class MangaDataClass:
	title: str
	desc: str
	url: str
	chapter: float
