import operator
import time
import os

import resources.constants as constants


def remove_trailing_zeros_if_zero(n):
    if is_float(n):
        if str(n).count(".") == 0 or str(n).endswith(".0"):
            return int(n)
        else:
            return float(n)
    return n


def is_float(f) -> bool:
    try:
        float(f)
    except ValueError:
        return False
    else:
        return True


def callback_once_true(master, search_obj, callback):
    if search_obj.finished:
        callback()
    else:
        master.after(100, callback_once_true, master, search_obj, callback)


""" Sorting functions"""


def sort_manga_by_title(manga):
    now = time.time()
    manga.sort(key=operator.attrgetter("title"))
    print(f">>> Sorting took {time.time()-now}s")
    return manga


def sort_manga_by_id(manga):
    now = time.time()
    manga.sort(key=operator.attrgetter("id"))
    print(f">>> Sorting took {round(time.time() - now, 2)}s")
    return manga


def get_latest_offline_chapter(title: str) -> float or int:
    manga_dir = os.path.join(constants.MANGA_DIR, title)

    if os.path.isdir(manga_dir):
        files = os.listdir(manga_dir)

        return max(map(lambda f: remove_trailing_zeros_if_zero(f.split()[-1].replace(".pdf", "")), files))

    return 0


"""
def getSortedMangaList(title: str) -> list:
	title = removeNastyChars(title)

	mangaPath = os.path.join(constants.MANGA_DIR, title)

	if (not os.path.isdir(mangaPath)):
		return None
	
	mangaList = sorted(os.listdir(mangaPath), key = lambda m: float(m.split("Chapter")[-1].replace(".pdf", "")))

	return mangaList
"""