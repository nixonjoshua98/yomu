import os

from database.database_enums import MangaStatusEnum


MANGA_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Downloaded Media", "Comics")
MANGA_STATUS = [e.prettify() for e in MangaStatusEnum]