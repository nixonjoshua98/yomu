import os

import resources.constants as constants

def removeNastyChars(string):
    return "".join([i for i in string if i not in ':\\/|*"><?.,'])


def getTotalAvailableChapters(title: str, latestChapter: str) -> int:
	title = removeNastyChars(title)

	mangaList = getSortedMangaList(title)

	if mangaList == None:
		return -1

	# Removes .0 from 4.0, 56.0 etc...
	latestChapter = splitChapter[0] if latestChapter.endswith(".0") else latestChapter

	chapterName = f"{title} Chapter {latestChapter}.pdf"

	try:
		total = len(mangaList) - (mangaList.index(chapterName) + 1)
	except ValueError: # If chapters read = 0 and no chapter 0
		return len(mangaList)
	else:
		return total


def getNextChapter(title: str, latestChapter: str) -> int:
	title = removeNastyChars(title)
	mangaList = getSortedMangaList(title)

	# Removes .0 from 4.0, 56.0 etc...
	latestChapter = splitChapter[0] if latestChapter.endswith(".0") else latestChapter

	chapterName = f"{title} Chapter {latestChapter}.pdf"

	print(mangaList[0])
	_id = mangaList.index(chapterName)

	return _id


def getLatestChapter(title: str, latestChapter: str) -> int:
	mangaList = getSortedMangaList(title)

	if mangaList == None:
		return -1

	x = mangaList[-1].split("Chapter")[-1].replace(".pdf", "")
	x = x.replace(".0", "")

	return x.lstrip()


def getSortedMangaList(title: str) -> list:
	title = removeNastyChars(title)

	mangaPath = os.path.join(constants.MANGA_DIR, title)

	if (not os.path.isdir(mangaPath)):
		return None
	
	mangaList = sorted(os.listdir(mangaPath), key = lambda m: float(m.split("Chapter")[-1].replace(".pdf", "")))

	return mangaList