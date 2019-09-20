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
	MangaStatusDC(key=5, 	text="Dropped",			downloadable=True),
	MangaStatusDC(key=5, 	text="Completed",		downloadable=True),
)


def get_all_downloadable(keys_only: bool = False):
	ls = list(filter(lambda s: s.downloadable, ALL_STATUS))

	if keys_only:
		return [i.key for i in ls]

	else:
		return ls
