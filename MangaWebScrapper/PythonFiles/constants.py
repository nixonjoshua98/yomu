import os
import enums

# - Manganelo constants

MANGANELO_BASE_URL = "http://manganelo.com/"
MANGANELO_SEARCH_URL = MANGANELO_BASE_URL + "search/"

# -

# - Ciayo constants

CIAYO_BASE_URL = "https://www.ciayo.com/en/"
CIAYO_SEARCH_URL = CIAYO_BASE_URL + "search?q="

# - Manga save constants

MANGA_SAVE_DIR = r"D:\Downloaded Media\Comics"

# -

# - Database constants

DB_PATH = r"D:\OneDrive - UoL\OneDrive - University of Lincoln\manga_database.sqlite3"
DB_CON_STR = "sqlite:///" + DB_PATH

# -

# - Interface constants

MANGA_STATUS = [e.prettify() for e in enums.MangaStatusEnum]

# -

# - Asset locations

CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "..", "Assets", "chromedriver.exe")

# -
