import operator


def sort_manga_by_title(manga):
    manga.sort(key=operator.attrgetter("title"))


def sort_manga_by_id(manga):
    manga.sort(key=operator.attrgetter("id"))


def sort_manga_by_latest_chapter(manga):
    manga.sort(key=operator.attrgetter("latest_chapter"), reverse=True)


def sort_manga_by_chapters_available(manga):
    manga.sort(key=lambda m: m.latest_chapter - m.chapters_read, reverse=True)
