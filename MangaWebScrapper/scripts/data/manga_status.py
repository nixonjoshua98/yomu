from dataclasses import dataclass


@dataclass
class MangaStatusDC:
	key: int
	text: str
	downloadable: bool


ALL_STATUS = (
	MangaStatusDC(key=0, 	text="Recently Added",	downloadable=True),
	MangaStatusDC(key=1, 	text="Favourites",		downloadable=True),
	MangaStatusDC(key=2, 	text="Reading List",	downloadable=True),
	MangaStatusDC(key=4, 	text="Dropped",			downloadable=False),
	MangaStatusDC(key=5, 	text="Completed",		downloadable=False),
)


def get_all_downloadable(keys_only: bool = False):
	ls = list(filter(lambda s: s.downloadable, ALL_STATUS))

	if keys_only:
		return [i.key for i in ls]

	else:
		return ls


def from_key(key: int):
	for s in ALL_STATUS:
		if s.key == key:
			return s
	return None