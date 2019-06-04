import database.enums

# - Manganelo constants

MANGANELO_BASE_URL = "http://manganelo.com/"
MANGANELO_SEARCH_URL = MANGANELO_BASE_URL + "search/"

# -

# - Manga save constants

MANGA_SAVE_DIR = r"D:\Downloaded Media\Comics"

# -

# - Database constants

DB_PATH = r"D:\OneDrive - UoL\OneDrive - University of Lincoln\manga_database.sqlite3"
DB_CON_STR = "sqlite:///" + DB_PATH

# -

# - Interface constants

MANGA_STATUS = [e.prettify() for e in database.enums.MangaStatusEnum]

# -
